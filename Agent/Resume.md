## 总结 1

### 点 1 — 精准撮合线索批量创建：并发管线 + 应用层去重 + 竞态收敛

What 

在 `create_lead_batch.go` 中实现了 `BatchCreateLead`：一次请求批量创建主播 PK 线索（lead）。核心是一个 固定 5 worker 的并发管线（`createLeadWorkerCount`），配合三层防重复机制：请求内去重、DB 层"存在即复用"、以及并发竞态下的"创建冲突→回查→复用"收敛逻辑。还包含 UID / handle 交叉引用的身份预解析（`resolveLeadAnchors`），解决同一主播既可用 UID 又可用 handle 传入时被算成两条线索的问题。

Why

线索是整个撮合系统的输入源，重复线索会污染下游推荐与配对，且批量入口天然面临并发。运营侧和算法定时任务可能对同一 `(anchor_uid, match_time_start)` 同时发起创建，若无收敛会产生重复行、误导撮合。这个设计把"正确性 + 吞吐 + 并发安全"三者在没有唯一约束 upsert 的前提下同时解决。

How

- 并发：`sync.WaitGroup` + 缓冲 channel + 5 个通过 `utils.SafeGo`（带 panic 恢复）启动的 worker；结果写入预分配、按 index 分区的 slice，无锁。
- 请求内去重：先 `resolveLeadAnchors` 把 handle 统一解析成 canonical UID（走 `rpc.GetUserIDByDisplayID` + `rpc.MGetHostInfoSync`），再按 `fmt.Sprintf("%d_%d", uid, matchTimeStart)` 建 `dupMap`，把首次结果扇出给重复位置。
- DB 竞态收敛：`createLeadForOperator` 先 `CheckLeadExist`（走 `simple_dal.CtxUseWrite` 主库读避免从库延迟），若命中直接复用并返回关系（`existingLeadNone/SameOperator/DifferentOperator`）；写入命中 `ErrLeadAlreadyExists` 时二次回查，若并发请求已建则复用，仅真正不可恢复错误才返回 `createLeadErrCodeInternalError`。
- 契约：错误码收敛为 `1=内部错误 / 2=非法主播`，通过 `errorSettable` 接口让批量与推荐两种结果共用一套 setter；"已被他人创建"用 `IsExist=true` 标记而非报错。

简历语言：

设计并实现主播线索批量创建服务，采用固定容量 worker 池（5 并发）+ 无锁分区写入的并发管线，将批量创建吞吐提升约 [填写真实数据]；针对无唯一约束场景，落地"请求内去重 + 主库存在性校验 + 创建冲突回查复用"三级竞态收敛机制，并通过 UID/handle 身份预解析消除跨标识重复，彻底消除重复线索。

### 点 2 — 周期赛批量建赛编排：管线复用 + 异步结果缓存 + 卡位调度

What 

在 `batch_create_pk_match_by_cohort.go` 及配套文件中实现"按人群包批量建赛"：对多个赛事配置扇出创建自动匹配任务，复用单场建赛的完整管线（校验→分配 ID→时间归一/重叠校验→人群规模检查→算起止时间→落库→建首场子赛→发起审批），并把批量结果写入 Redis 供独立 RPC 轮询获取。

Why 

批量建赛一次可能创建大量比赛，同步返回会超时；且必须与单场建赛行为完全一致以免逻辑漂移。将结果异步缓存 + 轮询解耦，既保证响应及时，又能让调用方按 `taskID` 拉取最终结果。同时批量场景直接复用单建管线，避免了双份易漂移的建赛逻辑。

How

- 结果缓存收敛进 biz 层，保证"处理结束后恰好缓存一次"；key 前缀 `pk_match_plaza:batch_create_pk_match_by_cohort_result`，TTL 72h，缓存失败仅打 `[ALERT]` 日志不阻断建赛（best-effort）。
- 轮询侧 `getBatchCreatePkMatchByCohortResultWithRetry`：最多 4 次、间隔 500ms，且 sleep 是 context 取消感知 的（`select` on `ctx.Done()`），并区分"redis 故障"与"结果未就绪/taskID 过期"两种语义。
- 调度采用"向后推比赛日、向前减启动点"卡位（`domain.GetAutoMatchTaskStartTime`）：`ImmediateExc` 为 true 时固定 `now+15min` 启动；否则由 `GetMatchStartDay` + `FindNextWeekday` 算出最早比赛日后，再按报名/直投提前天数回退启动时间；人群未就绪时 `+1` 天为受众包计算留缓冲。
- 主从一致性：首场子赛创建紧接父任务落库，通过新增 `GetMatchTaskByMaster`/`GetAutoMatchListByMaster`（`simple_dal.CtxUseWrite`）走主库读，修复从库延迟导致的 record-not-found。

简历语言：

主导按人群包批量建赛能力，复用单场建赛全链路管线避免逻辑分叉，通过 Redis 异步结果缓存（72h TTL）+ context 感知的重试轮询将批量建赛改造为非阻塞异步流程，并明确区分基础设施故障与任务未就绪两类状态；实现"向后推比赛日、向前减启动点"的时间卡位调度，并以主库读修复首场子赛的主从延迟问题。

### 点 3 — 双语错误分类体系：类型化标签解耦内部错误与用户文案

What 

在 `send_intent_error.go`、`rena_callback.go` 中设计了一套错误分类→中英双语文案的映射体系。业务校验失败时给 `werror` 挂类型化分类标签（`operator_missing / not_sender / lead_invalid / already_sent`），回调层据此回填 `ErrorMessage`（英）与 `ErrorMessageZh`（中），未命中走兜底文案。该分类后来被推荐卡失败通知（红色失败卡片）复用。

Why

内部错误是给开发看的英文串，直接抛给终端用户（尤其国际化 Lark 卡片场景）体验极差。传统做法靠字符串匹配 message 脆弱且易碎（`werror.Is` 只比状态码、无法区分同码错误）。用类型化标签把"内部错误"与"用户可见文案"彻底解耦，既保证国际化文案一字不差，又让新增分类只需加映射项。

How

- 分类枚举 `sendIntentErrKind` + `sendIntentErrMsgMap`（EN/ZH 结构体表）+ `sendIntentErrDefault` 兜底。
- `tagSendIntentErr(wErr, kind)` 把分类写进 `werror.Extra`（key `rena_callback_err_kind`），`extractSendIntentErrKind` 带 nil / 类型安全地读回——绕开了 `werror.Is` 无法区分同状态码错误的限制。
- 校验点统一打标（如 `validateIntentLeads` 6 个 return 在调用处统一包裹为 `lead_invalid`），回调分支 `fillSendIntentErrMsg` 回填双语。
- 复用性：`biz_callback_error_card.go` 的 `sendIntentFailureReason` 直接复用同一套 `extractSendIntentErrKind`+`sendIntentErrText`，一套分类同时服务同步返回与异步失败卡片两条路径。

简历语言：

设计类型化错误分类体系，通过在错误对象 Extra 上挂分类标签、映射为中英双语文案，彻底解耦内部开发者错误与国际化用户提示，规避了框架层"同状态码错误无法区分"的限制；该分类被同步接口与异步失败卡片两条链路复用，新增错误类型仅需扩展映射表。

### 点 4 — 区域×成长层 P50 阈值查询 API：配置驱动的多源数据检索

What 

在 `get_anchor_region_grow_layer_p50_threshold.go` 与 `data_retrieve.go` 中实现了按"运营区域 × 主播成长层"返回 PK 场次/收入 P50（中位数）基线的查询接口，输出为嵌套 map `map[region]map[layer]*P50Threshold`。用一张 2×2 配置矩阵（成长层类型 动态/静态 × 分层模式 阶段/群组）选择对应的离线数据表与列名。

Why 

P50 阈值是撮合公平性的统计基准——给定区域与成长层，用中位数活跃度/收入判断主播是否达标、如何公平配对。但四种分层策略各自落在不同 schema 的离线表（列名甚至不同，如 `avg_pk_cnt_p50` vs `avg_live_pk_cnt_p50`）。配置驱动让"新增一种分层组合"从改逻辑降级为改数据。

How

- 配置矩阵 `anchorRegionGrowLayerP50ThresholdConfig`（itemID/apiName/各列名），`getAnchorRegionGrowLayerP50ThresholdConfig(type, mode)` 嵌套 switch 选择；非法组合返回明确错误。
- 结果解析 `parseAnchorRegionGrowLayerP50ThresholdResults` 对平台返回的 `[][]string` 做 schema 无关的按列名解析：`normalize`（小写、去 `_`/`-`）匹配列，做列缺失/行宽/非数值的严格校验，把上游 schema 问题显式暴露为错误而非静默补零。
- 两级过滤：biz 层按请求的 region 集合 + grow-layer 集合过滤（`map[string]struct{}`），并强制两者非空校验，避免全表下发。
- IDL 精简（`d02ab463`）：`P50ThresholdData`→`P50Threshold`，去掉与 map 键重复的 `RegionCode/GrowLayerValue`；`GrowLayerMode_Diamond`→`Group` 对齐产品语义。

简历语言：

设计并实现按"区域×主播成长层"查询 PK P50 基线的撮合数据接口，用 2×2 配置矩阵屏蔽 4 张异构离线表的差异，使新增分层策略从改代码降为改配置；实现 schema 无关的按列名解析与列缺失/行宽/类型的严格校验，将上游数据问题显式化，并通过 IDL 去冗余精简了传输结构。

### 点 5 — 算法驱动的对手推荐 + 时间对齐意向撮合流程

What 

在 `send_recommend.go`、`lead_algo_recommend.go`、`send_intent_time_aligned.go` 中实现了完整的"创建线索→算法推荐对手→发起意向→撮合"交互闭环：`CreateLeadAndGetRecommend` 同步返回排序后的对手推荐；推荐/意向经双语 Lark 卡片触达；当对手比赛时间与源线索不一致时自动克隆并对齐时间再发意向。

Why 

这是撮合系统面向运营的核心交互路径。推荐要快（同步返回而非等异步卡片）、要稳（算法结果缓存防重复计算）、要正确（时间不一致不能直接失败，而应对齐；并发发起不能重复建线索）。它把算法能力、缓存、并发安全、国际化触达串成一条可用的业务闭环。

How

- 推荐引擎 `TriggerLeadAlgoRecommend`：取候选池（`GetActiveLeadsForAlgo`，精确时间优先、就近 5 个兜底）→ 调 `rpc.ArenaPKLead` 算法 → 按 Rank 排序 → 结果 JSON upsert 进缓存表；24h TTL + Redis SETNX 刷新锁（`tryAsyncRefreshAlgo`，5min）防缓存过期时的惊群重算。
- 批量 OpenID 解析：一次 `rpc.MGetAvatarUrlAndOpenID` 解析全响应的运营者 OpenID，规避 N+1。
- 时间对齐 `syncLeadMatchTime`：时间一致直接复用；否则先 `reuseAlignedLead`（存在即复用），再 `createAlignedLead` 克隆源线索并置为对手时间；创建失败回退再查一次，若并发已建则复用、吞掉错误。
- 触达：卡片走 `context.WithoutCancel(ctx)` + `SafeGo` 使其生命周期超过 RPC 响应；按对手时间是否一致选择 `send_intent` 或 `send_intent_time_aligned` 回调按钮。

简历语言：

搭建"建线索→算法推荐→意向撮合"交互闭环，`CreateLeadAndGetRecommend` 同步返回排序后的对手推荐；推荐引擎以 24h 缓存 + Redis SETNX 刷新锁抵御缓存过期惊群，并批量解析 OpenID 消除 N+1；针对对手比赛时间不一致场景实现自动克隆对齐 + 并发创建回退复用，使撮合成功率与体验显著提升 [填写真实数据]。

## 总结 2

### 一、模块定位

这是一个主播（anchor/creator）精准撮合业务模块，运行在 TikCast 直播中台，基于 Go + Kitex/Thrift。核心是把"运营为主播找 PK 对手"这件事拆成三层数据模型串起来的流水线：

- Lead（线索）：`models.AnchorPkLead`，一条"某主播在某时间点想打 PK"的意向声明（UID、开赛时间、时区、钻石档位、轮次、是否用道具/团播等）。
- Intent（意向）：`models.AnchorPkIntent`，运营 A 向运营 B 的某条 lead 发起的撮合邀约（src_lead → dst_lead）。
- PreciseMatch（精准匹配/赛事）：`models.AnchorPkMatch`，意向被接受后真正落地的一场 PK 赛事。

三层之间由 `PreciseMatchCreateWay` 枚举标识来源：`Direct`（直接建赛）/ `FromLead`（线索转赛）/ `FromIntent`（意向转赛）。

### 二、每个核心文件的功能职责

#### 1. `create_lead.go` — 单条线索创建
- 入口 `CreateLead`（`create_lead.go:31`）→ `createLeadWithSource`（:37），运营手工创建，来源 `LeadSourceOpManual`。
- `CreateLeadForAgent`（:171）：AI Agent 批量创建入口，逐条 `createLeadForAgentItem`，来源 `LeadSourceAgentAutoImport`。
- 关键业务规则：
  - 参数校验 `validateCreateLeadParams`（:475）：开赛时间必须 ≥ now + 1h（`MinMatchTimeDelayHours`），钻石 ≤ 10 位（`MaxLeadDiamonds = 9_999_999_999`）。
  - 主播有效性 `isValidCreateLeadHostInfo`（:216）：只接受 `AnchorType_UGC/AM/CM`。
  - 幂等：`GetLeadByAnchorUIDAndMatchTime` 查重，同主播+同开赛时间已存在则报 `ErrLeadAlreadyExists`（:62-64）。
  - 数据富化：并行拉 `MGetHostInfoSync`（主播基础信息）、`GetTradeUnionBaseInfoWithCache`（30 天 PK 次数/收入）、`GetAvgAcu30d`（30 天平均在线人数），失败仅 warn 不阻断（fail-open）。
  - `MapDiamondsToRange`（:498）把钻石数映射成 6 档 `DiamondsRange`。
  - 创建成功后 `CreateLead` 只异步触发算法推荐 `triggerLeadAlgoRecommendAsync`（:166），不发 bot 卡片；`CreateLeadForAgent` 则会 `triggerSendRecommendCard` 发推荐卡（:210）。
  - `formatAgentAnchorLanguages`（:435）：Agent 传入 "Accept all languages" 时落地成 62 种语言的默认 JSON（`defaultAgentAnchorLanguagesJSON`）。

#### 2. `create_lead_batch.go` — 批量线索创建 + 并发/去重
- 三个入口：`BatchCreateLead`（:76，Agent 批量）、`CreateLeadAndGetRecommend`（:176，创建并同步返回推荐结果）、以及内部复用的 `processBatchCreateLead`。
- 亮点设计：
  - `resolveLeadAnchors`（:57）预解析 handle→UID 身份，失败的行提前标错并 skip。
  - `dedupLeads`（:39）按 `(anchor_uid, match_time_start)` 去重，`dupMap` 让重复行复用首次结果（:120-122）。
  - 固定 `createLeadWorkerCount = 5` 的 worker 池 + channel 分发 + `sync.WaitGroup` 并发建线索（:103-118），用 `utils.SafeGo` 防 panic 扩散。
  - `createLeadForOperator`（:328）：先 `CheckLeadExist`，命中 `existingLeadWithDifferentOperator` 时也算成功并返回已存在 leadID（打 `IsExist=true` 标记，:145），发"已存在"变体卡片。这里有二次 `CheckLeadExist` 兜并发（:363）——处理 `ErrLeadAlreadyExists` 竞态。
  - `mapRecommendOperatorNameToOpenID`（:424）：一次性把推荐结果里的运营名批量换成飞书 OpenID（`MGetAvatarUrlAndOpenID`），供"联系运营"按钮跳转。

#### 3. `import_and_check_lead_file.go` + `import_and_check_lead_file_exec.go` — 文件导入 + 多级校验
- 入口 `ImportAndCheckLeadFile`（`..._file.go:15`）：五步流水线——解码 → 裁剪数据行 → 逐行校验 → （全部通过才）事务导入 → 触发推荐。
- `decodeLeadImportDocContent`（`..._exec.go:107`）：`base64 → urldecode → json`，带三重限流 `maxDocContentLen=2MB` / `maxDecodedBytesLen=4MB` / `maxRows=2000`。兼容 `[][]string` 和 `[][]interface{}` 两种 JSON 形态（飞书单元格可能是富文本对象，`normalizeLeadImportCellValue` 处理 map 的 `text` 字段）。
- `detectLeadImportDocFormat`（:244）：新旧模板双版本兼容——通过表头是否含 "creator uid" 判断 legacy（11 列/3 表头行/含 UID 列）还是 current（10 列/2 表头行/无 UID 列），用 `dataOffset()` 抹平列偏移。
- `parseLeadImportRow`（:271）：单行累积式校验，一次返回所有错误原因（避免运营反复提交）。`parseLeadImportMatchTime`（:543）同时支持 Excel serial 日期数字（基准 1899-12-30）和 5 种人类可读 layout。
- 校验层次（`..._file.go:55` `validateLeadImportRows`）：文件内查重 → 身份解析 `resolveLeadImportIdentity`（UID/handle 双向校验、必须匹配）→ 运营邮箱前缀批量校验 `MValidateUserEmailPrefixes` → DB 现存 active 线索查重。
- `importValidatedLeadRows`（`..._exec.go:467`）：全通过才在单事务里逐条 `ImportLeadFromTemplateWithoutRecommend` 导入（全成功或全失败），事务提交后再根据白名单 `IsUserInImportLeadsWhiteList` 决定是发推荐卡还是仅异步跑算法。

#### 4. `batch_create_precise_match_*.go` — 批量建赛（飞书 sheet 直建赛事）
- `batch_create_precise_match_doc.go`：入口 `BatchCreatePreciseMatchByDoc`（:26），从飞书文档链接直接批量建赛。
  - `resolveBatchMatchSpreadsheetToken`（:101）用正则 `batchMatchDocTokenPattern` 提取 token，`/wiki/` 链接需调 `GetWikiNodeObjToken` 解析并校验 objType 确为 sheet。
  - `readBatchMatchSheetRows`（:131）支持从链接锚点 `?sheet=` 或 fragment `#sheet=` 取 sheetID，读区间刻意"多读一行"以便正确报告"超出行数上限"而非静默截断（:143 注释）。
- `batch_create_precise_match_row.go`：模板列布局（A=UID A, B=UID B, C=时区, D=开始, E=结束, F=轮次），`parseBatchMatchRow`（:150）做 L1 解析 + L2 业务规则，`parseBatchMatchTime`（:266）同样兼容 Excel serial 与多 layout。`batchMatchMaxRows = 200` 防同步超时。
- `batch_create_precise_match_exec.go`：校验分层 L1（本地解析）/L2（业务规则）/L3（批量 IO：`validateBatchMatchAnchors` 一次性拉全部主播、`validateBatchMatchDuplicateInFile` 文件内查重）。`createBatchMatchRows`（:133）用 `errgroup` + `SetLimit(batchMatchCreateConcurrency=10)` 并发建赛，单行失败只记结果不中断整批。`convertBatchMatchConflictItems`（:212）把 pk_core 的档期冲突结构按"冲突方"聚合成前端明细。
- `batch_create_precise_match_reason.go`：错误目录 `batchMatchReasonCatalog`，每个 reason 带 `Code`（日志聚合）+ `FailType`（IDL 分类枚举）+ `Message`（透出运营）。

#### 5. `create_precise_match.go` — 建赛核心（分布式事务 + 补偿回滚）
`createPreciseMatchWithConflictDetail`（:31）是全模块最复杂的编排，8 步 + defer 回滚：
- Step 0 `validatePreciseMatchSourceStatus`（:276）：校验源 lead/intent 状态仍有效。
- Step 1 建 DB 记录（status=WaitingToPublish）。
- Step 2 `PreciseMatchPkCoreReserveWithConflict`（:76）：调 pk_core 占档期，失败直接删记录；成功后注册 `pkCoreReserveRollback` 补偿函数。
- Step 3 建 participants + activity。
- Step 4 更新运营区域。
- Step 5 `MarkLeadAsMatched`（:138）把 lead/intent 状态推到 matched（与 lead 的 Matched 同事务）。
- Step 6 `SubmitPreciseMatchApproval` 提交动态审批矩阵。
- Step 7 status → InApproving。
- Step 8 发建赛成功卡片给相关运营。
- 补偿回滚设计：`defer`（:87）在 `retErr != nil` 时依次撤销审批（`CancelApproval`）、释放 pk_core 占档、`rollbackPreciseMatchCreateData`（:186）在事务里回滚 participants/activity/match 状态，并按 createWay 把 lead/intent 状态改回 Active/Pending。
- `adjustCreateWayForLeadConversion`（:319）：容错——若 srcLeadID 缺失或主播对不上 lead，自动降级为 `Direct` 建赛而非报错。

#### 6. `send_intent.go` — 发送意向
- `SendIntent`（:29）：校验运营名 = srcLead 运营名（`sendIntentErrNotSender`）、两条 lead 同开赛时间、非 self、状态有效 → `createIntentAndSendCards`。
- `createIntentAndSendCards`（:145）：`GetPendingIntentBySrcDst` 防重复发送（`sendIntentErrAlreadySent`），建 intent（`RemindCount=1`），`SendIntentCard` 分别发给对方运营和自己（双卡）。
- `RemindIntentCard`（:224）：给定时提醒 job `ScanIntentRemindJob` 用的"只发卡不建 intent"路径，校验失败返回哨兵错误 `ErrIntentNotRemindable`（:27），调用方据此决定是否自增 `remind_count` 消耗触达配额。
- `buildIntentCardParams`（:280）构造双语意向卡，含跳回 Match Plaza 的 URL。

#### 7. `send_recommend.go` — 推荐对手卡片（纯手写飞书卡片 JSON）
- `SendRecommendCard`（:31）：拉 srcLead、补主播 handle、补推荐行运营 OpenID，`buildRecommendCard`（:130）用 `map[string]any` 手工拼飞书卡片 schema 2.0（含 header/body/config、中英 i18n）。
- 两个变体 `recommendCardVariantNormal` / `recommendCardVariantExisting`（:20）：普通推荐 vs "该时段已被其他运营创建线索"，intro 文案里明确出现 "Rena 已识别到你发布的寻找对手信息…"（:283-287）。
- 关键交互逻辑 `buildRecommendOperatorButtonRow`（:388）：同开赛时间→"直接发送意向"按钮（action=`send_intent`）；不同时间→"修改到对方时间并发送意向"按钮（action=`send_intent_time_aligned`），加一个"联系运营"跳飞书私聊按钮。回调按钮 payload 是 `{action, params:{src_lead_id, dst_lead_id}}`（:441-449）。

#### 8. `lead_algo_recommend.go` — 算法推荐对接（pk_core.ArenaPKLead）
- `TriggerLeadAlgoRecommend`（:167）：加载主 lead + 候选池（`GetActiveLeadsForAlgo` 保证同时间点优先、兜底最近 5 条）→ 调 `rpc.ArenaPKLead` 算法 → 按 Rank 排序 → 结果 JSON `UpsertLeadAlgoRecommend` 落库缓存。
- 读写分离缓存：`GetLeadAlgoRecommend`/`GetAlgoRecommendByLeads` 读缓存，`AlgoRecommendTTL = 24h`，过期时 `tryAsyncRefreshAlgo`（:36）用 Redis SETNX 锁（`algoRefreshLockTTL=5min`）防惊群打穿下游算法。
- `isOpponentLeadStillValid`（:365）读路径消毒：过滤掉缓存后已失效（非 Active/已过开赛时间）的对手。
- `rankReasonDisplayName`（:339）把算法返回的 `RankReason` 枚举（历史 PK、送礼者相似度、PK 收入相似、ACU 相似、开播时长相似等 8 种）映射成前端英文标签。

#### 9. `rena_callback.go` + `rena_callback_send_intent.go` — AI Agent (Rena) 回调
- `RenaCallback`（`rena_callback.go:23`）：AI Agent "Rena" 的动作回调入口，用 `renaCallbackHandlers` map 按 `ActionKey` 分发（`send_intent` / `send_intent_time_aligned`）。返回 `RenaCallbackStatus`（SUCCESS/FAILED/UNKNOWN）+ 中英双语 `error_message`（供 Agent 对话展示）。
- `newSendIntentCallbackHandler`（`..._send_intent.go:22`）：闭包适配器，把 Rena 的 params(JSON) 解析成 `SendIntentRequest`，`UserName` 直接取 `req.GetUserName()`（Agent 已带运营身份）。

#### 10. `biz_callback.go` + 子文件 — 飞书卡片按钮回调
- `BizCallback`（`biz_callback.go:28`）：飞书卡片（Interactive Card）按钮回调统一入口。双路由设计：先用 `parseBizActionValue` 试解析 `{action, params}` 格式（推荐卡按钮）分发到 `bizCallbackHandlers`；未命中则回退 `HandleIntentBizCallback` 处理老的 `IntentButtonInfo`（accept/reject）语义。
- `biz_callback_handle_recommend.go` `newBizSendIntentHandler`（:18）：BizCallback 拿不到点击者邮箱，故反查 srcLead 的 OperatorName 兜出运营身份（:29-37）；发送失败时 `notifySendIntentFailure` 发失败卡。
- `biz_callback_handle_intent.go` `parseIntentButtonInfo`（:39）：三层容错解析 ActionValue——直接反序列化 → 从 map 取 callback 字段 → 二次反序列化 string 包裹的 JSON，兼容飞书卡片不同版本的回调结构。

#### 11. `handle_intent_callback.go` — 意向 accept/reject 处理
- `HandleIntentCallback`（:24）：一堆前置校验（intent 必须 Pending 防重复点击 `FailedReasonLeadDuplicateClick`、开赛时间 ≥ now+30min、两 lead 都 Active、两 lead 同开赛时间）→ 分派 accept/reject。
- `handleIntentAccept`（:81）：构造 `FromIntent` 的建赛请求（结束时间 = 开始 + 1800s）调 `CreatePreciseMatch`，intent 状态由建赛事务内 `MarkLeadAsMatched` 推进，不重复 update（:96 注释）。
- defer `notifyIntentAcceptFailure`（:49）：失败时给对方运营发配对失败卡。

#### 12. `check_anchor_time_conflict.go` — 档期冲突检测
- `CheckAnchorTimeConflict`（:16）：批量检查一组主播在给定时间段是否已有 PK 档期冲突。
- `checkAnchorTimeConflictWithPkCore`（:52）：为每个主播构造 `OpPkPairItem`（`PkType_PkSingle`）调 `CheckPkTaskPkPairBySingleHost`，用 `FilterPkCoreBizErr` 过滤业务错误，把真实冲突的主播 UID 标 true 返回 map。

#### 13. `send_intent_time_aligned.go` — 时间对齐后发意向
- `SendIntentTimeAligned`（:14）：当我方 lead 与对方 lead 开赛时间不一致时，`syncLeadMatchTime`（:45）把我方时间对齐到对方——优先复用已存在的对齐 lead（`reuseAlignedLead`，:75，兼容 same/different operator），没有才新建（`createAlignedLead`，:96，来源 `LeadSourceSystemTimeAligned`）。
- 并发容错：`createAlignedLead` 建失败时再 `reuseAlignedLead` 一次兜并发创建的竞态（:119-123）。

### 三、核心业务全链路

```
① 线索产生（三条路径）
   ├─ 运营手工：CreateLead
   ├─ 文件导入：ImportAndCheckLeadFile（Excel/飞书模板，多级校验+事务导入）
   └─ AI Agent：CreateLeadForAgent / BatchCreateLead / CreateLeadAndGetRecommend
                    ↓
② 算法推荐：triggerLeadAlgoRecommendAsync → TriggerLeadAlgoRecommend
            → rpc.ArenaPKLead(pk_core) 算对手 → 结果落库缓存(24h, SETNX防惊群)
                    ↓
③ 推荐触达：SendRecommendCard 发飞书交互卡（Rena 署名），卡上带
            "直接发送意向" / "修改到对方时间并发送意向" 按钮
                    ↓
④ 发送意向（两个触发源汇聚）：
   ├─ Rena Agent 回调：RenaCallback → send_intent(_time_aligned)
   └─ 飞书卡片按钮回调：BizCallback → send_intent(_time_aligned)
        → SendIntent / SendIntentTimeAligned（时间不一致先对齐）
        → 建 AnchorPkIntent(Pending) + 发双语意向卡给对方运营
                    ↓
⑤ 意向应答回调：BizCallback → HandleIntentBizCallback → HandleIntentCallback
   ├─ Accept → handleIntentAccept → CreatePreciseMatch(FromIntent)
   └─ Reject → handleIntentReject（发拒绝卡）
                    ↓
⑥ 建赛落地：createPreciseMatchWithConflictDetail（8步分布式事务）
   建DB → pk_core占档(冲突检测) → participants/activity → MarkLeadAsMatched
   → 提交审批 → InApproving → 发建赛成功卡；任一步失败 defer 补偿回滚全链路

另有旁路：BatchCreatePreciseMatchByDoc（飞书 sheet 直接批量建赛，跳过 lead/intent）
```

### 四、rena_callback vs biz_callback 是什么

两者都是"用户点了推荐卡上的按钮，要发送意向"的回调，但触发通道和上下文不同：

- rena_callback = AI Agent「Rena」的动作回调。Rena 是一个智能体（推荐卡片 intro 明确写着 "Rena has detected your message looking for opponents…"）。当运营在飞书里跟 Rena 对话说"帮我找对手/发意向"，Rena 侧会回调本服务的 `RenaCallback`，`ActionKey` = `send_intent`/`send_intent_time_aligned`，params 是 JSON 字符串 `{src_lead_id, dst_lead_id}`，`UserName` 由 Agent 带过来。返回值是结构化的 `RenaCallbackStatus` + 中英双语 error_message（`fillSendIntentErrMsg`，`send_intent_error.go:56`），因为要回显在 Agent 对话里。

- biz_callback = 飞书交互卡片（Interactive Card）按钮的原生回调。运营直接点卡片上的按钮触发，`BizCallback` 收到 `ActionValue`。两者复用同一批业务函数（`SendIntent`/`SendIntentTimeAligned`），但 biz_callback 的关键差异是拿不到点击者邮箱，所以要反查 srcLead 的 OperatorName 来补运营身份（`biz_callback_handle_recommend.go:29`）。

设计上二者都用同名 action 常量 + handler map 分发（`renaCallbackHandlers` / `bizCallbackHandlers`），且 action key 与 `send_recommend.go` 生成按钮时写入的 `recommendCardActionSendIntent` 完全对齐，形成"发卡→点按钮→回调分发"的闭环。

### 五、可写进简历的技术亮点

1. 文件导入 + 多级校验流水线（可直接量化）
- 三层校验（本地解析 → 批量 IO → DB 查重）+ 单行累积式错误收集，一次返回全部原因避免运营反复提交（`import_and_check_lead_file_exec.go:271`）。
- 新旧模板双版本自动兼容：靠表头 "creator uid" 探测 legacy(11列)/current(10列) 并用 `dataOffset()` 抹平列偏移（`..._exec.go:244`）。
- Excel serial 日期解析：基准 1899-12-30 + 分数部分换算秒，同时兼容 5 种人类可读 layout（`..._exec.go:543`）；解码链 `base64→urldecode→json` 带 2MB/4MB/2000 行三重限流防打爆（`..._exec.go:107`）。
- 全量校验通过才在单事务导入（全成功/全失败一致语义），`import_and_check_lead_file_exec.go:467`。
- 批量建赛版从飞书文档链接直取数据：正则解析 token、wiki 节点类型校验、`?sheet=`/`#sheet=` 锚点定位、故意多读一行以正确报"超上限"（`batch_create_precise_match_doc.go:101/131/143`）。

2. 算法推荐对接 + 缓存治理
- 对接 pk_core `ArenaPKLead` 算法，8 类 `RankReason` 枚举映射为可展示标签（`lead_algo_recommend.go:339`）。
- 读写分离 + Redis SETNX 分布式锁防缓存击穿惊群（TTL 24h，刷新锁 5min，`lead_algo_recommend.go:36`），读路径二次消毒过滤已失效对手（:365）。

3. 事件驱动 / 异步 + 并发
- `utils.SafeGo` + `context.WithoutCancel` 做 fire-and-forget 异步推荐与发卡，脱离请求生命周期（`create_lead_batch.go:170`、`lead_algo_recommend.go:211`）。
- worker 池（channel + WaitGroup，`create_lead_batch.go:103`）与 `errgroup.SetLimit(10)`（`batch_create_precise_match_exec.go:143`）两种并发模型，单条失败不影响整批。
- `(anchor_uid, match_time_start)` 去重 + dupMap 复用结果（`create_lead_batch.go:39`）。

4. AI Agent (Rena) 集成 + 双回调通道统一
- Rena 智能体动作回调与飞书原生卡片回调复用同一批业务逻辑，用 action→handler map 分发（`rena_callback.go:18`、`biz_callback.go:21`）。
- Rena 回调返回结构化状态 + 中英双语错误文案，用 `werror.WithExtra` 挂错误分类标签再回填双语文案的解耦设计（`send_intent_error.go:48`）。
- biz_callback 三层容错解析飞书 ActionValue，兼容多版本卡片结构（`biz_callback_handle_intent.go:39`）。

5. 时间对齐 / 档期冲突检测
- 撮合双方开赛时间不一致时，自动"复用优先、无则新建"对齐 lead，并处理并发创建竞态（`send_intent_time_aligned.go:45/96`）。
- 基于 pk_core 的批量档期冲突检测，把冲突方按 BizPkId+TaskId 聚合成运营可读明细（`check_anchor_time_conflict.go:52`、`batch_create_precise_match_exec.go:212`）。

6. 交互卡片（Interactive Card）设计
- 纯 Go `map[string]any` 手写飞书 schema 2.0 卡片，全量中英 i18n、column_set 布局、callback/multi_url 双按钮类型（`send_recommend.go:130`）。
- 按时间是否对齐动态渲染不同按钮/动作（`buildRecommendOperatorButtonRow`，`send_recommend.go:388`）；失败场景独立红色失败卡带跳转按钮（`biz_callback_error_card.go:117`）。

7. 幂等 / 容错 / 分布式事务补偿
- 建赛 8 步编排 + defer 补偿回滚（撤审批、释放 pk_core 占档、事务内回滚 lead/intent 状态），`create_precise_match.go:87/186`。
- lead 创建幂等：同主播+同开赛时间去重（`create_lead.go:58`、`import_lead_from_template.go:88`），并发下二次 CheckLeadExist 兜竞态（`create_lead_batch.go:363`）。
- intent 防重复点击（Pending 状态机 + `GetPendingIntentBySrcDst`，`handle_intent_callback.go:55`、`send_intent.go:147`）。
- 数据富化 RPC 全部 fail-open（失败仅 warn 用默认值，不阻断主流程）。
- 哨兵错误 `ErrIntentNotRemindable` 区分"业务跳过（消耗配额）"与"系统错误（下 tick 重试）"（`send_intent.go:27/224`）。

## 总结 3

### 一、旗舰项:主播 PK「精准撮合」全链路(Lead → Intent → Match)

功能逻辑
把"运营为主播找 PK 对手"抽象成三层数据模型的流水线:`Lead(线索)` → `Intent(意向)` → `PreciseMatch(赛事)`,并用 `PreciseMatchCreateWay` 枚举(`Direct/FromLead/FromIntent`)贯穿溯源。线索有三条产生路径(运营手工 / 文件导入 / AI Agent),经算法推荐 → 发卡触达 → 发送意向 → 意向应答 → 建赛落地,形成闭环。见 `create_precise_match.go`、`handle_intent_callback.go`。

技术亮点
- 建赛核心 `createPreciseMatchWithConflictDetail` 是一个 8 步分布式事务编排 + defer 补偿回滚(Saga):建 DB → pk_core 占档期 → 建 participants/activity → 更新区域 → `MarkLeadAsMatched`(与 lead 状态同事务) → 提交审批 → 置 `InApproving` → 发卡;任一步失败,`defer` 依次撤销审批、释放 pk_core 占档、在事务内把 lead/intent 状态回滚回 `Active/Pending`。见 `create_precise_match.go:87-184` 与回滚事务 `create_precise_match.go:186-242`。
- 全链路幂等:线索按 `(anchor_uid, match_time_start)` 去重、意向靠 `Pending` 状态机 + `GetPendingIntentBySrcDst` 防重复点击、并发下二次 `CheckLeadExist` 兜竞态。

意义价值
把一个涉及"外部算法 + 档期占用 + 审批 + 多方通知"的多阶段、易产生脏数据的建赛动作,做成了最终一致、可回滚、可追溯来源的可靠流程,直接支撑运营侧的核心撮合转化。

### 二、AI Agent(Rena)集成 + 双回调通道统一分发

功能逻辑
主播撮合接入了智能体 Rena:运营在飞书里跟 Rena 对话找对手,Rena 回调本服务发起意向;运营也可以直接点飞书推荐卡上的按钮触发。两条通道(`RenaCallback` / `BizCallback`)最终汇聚到同一批业务函数(`SendIntent` / `SendIntentTimeAligned`)。见 `rena_callback.go`、`biz_callback.go`。

技术亮点
- action → handler map 分发统一两种回调,且 action key 与发卡时写入按钮的常量严格对齐(`send_intent`/`send_intent_time_aligned`),形成"发卡 → 点按钮 → 回调"闭环 `rena_callback.go:18-21`。
- `BizCallback` 采用双路由 + 回退:先试解析 `{action, params}` 新格式,未命中回退到老的 `IntentButtonInfo`(accept/reject)语义 `biz_callback.go:28-49`;老回调再叠三层容错解析,兼容飞书多版本卡片结构。
- Rena 回调返回结构化状态 + 中英双语 error_message(用 `werror` 挂错误分类标签再回填双语文案),供 Agent 对话直接展示。

意义价值
体现了 LLM Agent 与传统业务系统的工程化对接能力——用统一契约同时服务"人点按钮"和"Agent 调动作"两种入口,是当下很有说服力的简历亮点。

### 三、批量建赛:并发批处理 + 结果异步分离(两个模块共用范式)

功能逻辑
支持运营一次性按人群包(cohort)或飞书表格批量创建几十上百场 PK 赛事。auto_match 侧 `BatchCreatePkMatchByCohort` 把 Agent 会话 ID 当 taskID,同步并发建赛后写 Redis,前端再轮询取结果;precise_match 侧 `BatchCreatePreciseMatchByDoc` 从飞书文档链接直接建赛。见 `batch_create_pk_match_by_cohort.go`。

技术亮点
- `errgroup.Group` + `SetLimit(10)` 控并发,goroutine 内永远 `return nil`——单场失败不熔断整批,失败明细各自回填 `batch_create_pk_match_by_cohort.go:51-62`。
- 结果与请求解耦:结果写 Redis(TTL 72h),用可取消(`select{ctx.Done()/timer.C}`)的 3+1 次、500ms 间隔重试轮询获取,规避同步长耗时超时。
- 错误码保真:用 `errors.As` 抽出 `werror.Error.StatusCode()` 回填结果,不丢错误类型 `batch_create_pk_match_by_cohort.go:270-277`。

意义价值
把运营的重复性批量操作从"逐个手工建"提升到"一键批量、部分失败可见、结果异步可查",是可量化效率提升的典型场景。

### 四、自动赛调度「卡位」机制(时间编排)

功能逻辑
自动赛需要按比赛日反推出"任务启动点、报名截止点、审批最晚点",并支持单期(Single)/周期(Weekly)两种周期。见 `batch_create_pk_match_by_cohort_validate.go`、`auto_match_get_match_task.go:105-136`。

技术亮点
- "向后推比赛日,向前减启动点":Weekly 场景下首期起点不足 24h 就整周顺延 `AddDate(0,0,7)`,windowEnd 因 weekday 排序倒挂时追赶到 start 之后 `batch_create_pk_match_by_cohort_validate.go:87-97`。
- 四段式时间校验管道:排序 → 基础(每 slot end>start) → 重叠检测 → 时间窗(24h 卡点 + 周期顺延)。
- 人群包未就绪时启动点额外 +1 天留缓冲,`ImmediateExc` 时固定 `now+15min`——把"故意放行/兜底"和"异常"用注释显式区分。

意义价值
调度时间是这类活动系统最容易出错、最难测的部分,做成分层可校验、边界清晰的机制,直接决定线上是否会出现"赛事排到过去/报名来不及"的事故。

### 五、文件导入多级校验流水线(Excel/飞书模板)

功能逻辑
运营上传 Excel/飞书模板批量导入线索或建赛,系统解析 → 逐行校验 → 全通过才事务导入。见 `import_and_check_lead_file.go`、`import_and_check_lead_file_exec.go`。

技术亮点
- 三层校验 + 单行累积式报错(本地解析 → 批量 IO 主播/运营校验 → DB 现存查重),一次返回全部原因,避免运营反复提交;错误目录用 `Code(日志聚合)+Category/FailType(分类)+Message(透出)` 三段式,见 `lead_import_reason.go`。
- 新旧模板双版本自动兼容:靠表头是否含 "creator uid" 探测 legacy(11列)/current(10列),用 `dataOffset()` 抹平列偏移。
- Excel serial 日期解析(基准 1899-12-30)+ 5 种人类可读 layout 兼容;解码链 `base64→urldecode→json` 带 2MB/4MB/2000 行三重限流防打爆。
- 全通过才在单事务导入(全成功/全失败一致语义)。

意义价值
面向非技术运营的导入功能,校验体验(一次报全 + 可读原因)和数据一致性(事务)都是真实痛点,工程含金量高且易讲清楚。

### 六、算法推荐对接 + 缓存治理

功能逻辑
对接 pk_core 的 `ArenaPKLead` 推荐算法为线索找对手,结果排序后落库缓存,读写分离。见 `lead_algo_recommend.go`。

技术亮点
- Redis SETNX 分布式锁防缓存击穿惊群:缓存(TTL 24h)过期时只放一个请求异步重算(刷新锁 5min),其余直接跳过 `lead_algo_recommend.go:36-50`。
- 读路径二次消毒 `isOpponentLeadStillValid`,过滤缓存后已失效(非 Active/已过开赛时间)的对手 `lead_algo_recommend.go:365-376`。
- 把算法返回的 8 类 `RankReason` 枚举(历史 PK、送礼者相似度、收入/ACU/开播时长相似等)映射为前端可展示标签。

意义价值
展示"业务系统正确对接算法 + 缓存穿透/一致性治理"的能力,是后端岗位很硬的加分项。

### 七、时间对齐 / 档期冲突检测 + 动态交互卡片

功能逻辑
撮合双方开赛时间不一致时,自动把我方时间对齐到对方;建赛前批量检测主播档期冲突;推荐卡按时间是否对齐渲染不同按钮。见 `send_intent_time_aligned.go`、`check_anchor_time_conflict.go`、`send_recommend.go`。

技术亮点
- 时间对齐"复用优先、无则新建",并处理并发创建竞态(建失败再复用一次) `send_intent_time_aligned.go:45-134`。
- 纯 Go `map[string]any` 手写飞书卡片 schema 2.0,全量中英 i18n;按开赛时间是否一致动态渲染按钮/动作(同时间→直接发意向,不同→改时间再发)。

意义价值
这些是撮合体验的"临门一脚"细节,能体现对业务边界(并发、时区、双方状态)的细致把控。

## 总结 4

### 一、一致性(Consistency)机制

这是主项一(建赛)的核心。这里的难点在于:一次建赛要跨 本地 DB + 外部 pk_core 占档 + 审批系统 三个独立资源,没有全局事务,必须自己保证"要么都成、要么都回滚"。

#### 1. Saga 编排 + 分层补偿(跨资源最终一致)
`createPreciseMatchWithConflictDetail` 的 8 步里,凡是有外部副作用的步骤都在成功后当场注册一个补偿闭包,再由统一的 `defer` 在 `retErr != nil` 时逆序执行:

- pk_core 占档成功后立即挂 `pkCoreReserveRollback`,失败时调 `DeletePkTaskPkPair` 释放档期 `create_precise_match.go:82-97`;
- 补偿顺序是"外部资源→本地状态":先撤审批(`CancelApproval`)、再释放 pk_core 占档、最后 `rollbackPreciseMatchCreateData` 把 participants/activity/match 和 lead/intent 状态回滚。

关键点是补偿不是简单 delete,而是按 `PreciseMatchCreateWay` 精确还原来源状态机:`FromLead` 把 lead 改回 `Active`,`FromIntent` 把 intent 改回 `Pending` 且两条 lead 都改回 `Active` `create_precise_match.go:219-235`。这样失败后系统回到"可被重新撮合"的干净态,而不是留下悬挂赛事。

#### 2. 用本地 DB 事务收敛"同生共死"的状态变更
凡是"必须同时成立"的多张表写,都收进一个 `simple_dal.DB(ctx).Transaction`,而不是分散更新:

- 接受意向时,`MarkLeadAsMatched` 把 intent 置 `Accepted` 和两条 lead 置 `Matched` 放同一事务 `precise_match.go:715-724`;
- 回滚同理走事务 `create_precise_match.go:191-238`。

这就是我在 `handle_intent_callback.go:96-98` 看到的注释所指:accept 路径不再单独 update intent,把状态推进的唯一权交给建赛事务,消除"intent 已接受但赛事没建成"的中间不一致窗口。

#### 3. 幂等 + 状态机前置校验,吸收重复/并发
一致性不止靠回滚,还靠不产生重复:

- 意向去重:发送前 `GetPendingIntentBySrcDst` 命中就直接返回 `sendInterErrAlreadySent`,不再建第二条 `send_intent.go:147-150`;
- 应答防抖:`HandleIntentCallback` 要求 intent 必须是 `Pending`,重复点击直接被 `FailedReasonLeadDuplicateClick` 挡掉 `handle_intent_callback.go:55-57`——用状态机把"双击/回调重投"变成幂等;
- 线索去重:`(anchor_uid, match_time_start)` 唯一,并发写靠"建失败后二次 `CheckLeadExist`"兜竞态(见 `send_intent_time_aligned.go:119-123` 的对齐 lead 复用)。

### 二、可靠性(Reliability)机制

可靠性的原则贯穿三个主项:核心事务要么成功要么干净失败;非核心副作用绝不拖垮核心。

#### 1. Fail-open 降级:区分"故意放行"与"异常中断"
数据富化类 RPC(主播信息、30 天 PK 数据、审批链接生成)全部失败即 warn + 用默认值继续,不阻断主流程。代码里这类"故意放行"都有明确注释与真正的异常处理区分开——比如意向卡发送失败时注释 `intent still created`,明确"卡没发出去不代表意向没建成" `send_intent.go:198-200`。这条边界很重要:能降级的降级,不能降级的(占档/落库)绝不降级。

#### 2. 退避重试:把"瞬时限流"和"真故障"分开处理
主项三的批量导入一次要取几万个 ID、还有 10 个 goroutine 并发取号,ID 服务限流是常态而非故障。`mGetIDWithRetry` 因此做了:

- 5 次退避重试,`backoff *= 2` 指数退避;
- 加随机抖动 `sleep = backoff + rand(backoff)`,防止同一时刻被限流的并发 goroutine"一起退避、一起重试"把拥塞原样复现 `id_generator.go:80-88`;
- 重试时监听 `ctx.Done()` 可中断。

理由代码注释讲得很直白:一次取号失败会让整个导入事务回滚,所以必须扛住瞬时限流 `id_generator.go:21-27`。通用 `utils.Retry` 也是同样的指数退避范式 `tool.go:34-49`。

#### 3. 异步任务的隔离:panic 兜底 + 脱离请求生命周期
所有 fire-and-forget(异步跑推荐、异步发卡、异步建 banner)都走 `utils.SafeGo`,内置 `recover`,单个后台 goroutine panic 不会打崩请求 `tool.go:28-33`。更关键的是用 `context.WithoutCancel(ctx)` 派生 context:主请求返回后 ctx 被 cancel,异步任务不受牵连仍能完成通知/落库(见 `lead_algo_recommend.go:211-222` 和批量 bot 通知的 `WithoutCancel + WithTimeout(1min)`)。

#### 4. 批量场景"部分失败不熔断"(主项三)
`errgroup` 里每个 item 的 goroutine 永远 `return nil`,失败信息回填各自的 result,而不是让 `eg.Wait()` 短路整批 `batch_create_pk_match_by_cohort.go:57-62`。并且失败时用 `errors.As` 抽出原始 `werror.StatusCode()` 回填,错误类型不丢失 `batch_create_pk_match_by_cohort.go:270-277`——运营能看到每一场到底为什么失败,而不是"整批失败"。

#### 5. 双回调通道的身份可靠还原(主项二)
飞书原生卡片回调(`BizCallback`)拿不到点击者邮箱,系统反查 srcLead 的 OperatorName 补出运营身份 `biz_callback_handle_recommend.go`,避免因为通道差异导致"谁发的意向"归属错乱;老版卡片 ActionValue 还做了三层容错解析兼容多版本结构。

### 三、低延迟(Low-latency)机制

低延迟的思路是:把慢的、可失败的东西移出关键路径;把批量并行化;把重复计算缓存掉。

#### 1. 读写分离缓存 + SETNX 防惊群(主项一/推荐链路)
算法推荐是重下游调用。这里做了:

- 结果 `UpsertLeadAlgoRecommend` 落库缓存,读路径 `GetAlgoRecommendByLeads` 直接命中,读不打算法;
- 缓存过期(TTL 24h)时用 Redis SETNX 锁(`algoRefreshLockTTL=5min`)保证同一 lead 只有一个请求触发异步重算,其余请求直接跳过,防止缓存失效瞬间惊群打穿下游算法 `lead_algo_recommend.go:36-50`;
- 关键:刷新是异步触发的,读请求立刻用旧缓存返回,不等重算——即 stale-while-revalidate,牺牲一点新鲜度换取稳定低延迟;
- 读路径还做二次消毒 `isOpponentLeadStillValid`,把缓存后已失效的对手就地过滤,不用回源。

#### 2. 同步/异步解耦 + 结果轮询(主项三)
批量建赛如果同步等所有赛事建完再返回,一定超时。这里把请求拆成两段:

- 建赛阶段并发执行后把结果写 Redis(TTL 72h),请求快速返回 taskID `batch_create_pk_match_by_cohort_result.go:45-60`;
- 前端用 `GetBatchCreatePkMatchByCohortResult` 轮询,取数用 3+1 次、500ms 间隔、可被 `ctx.Done()` 打断的 `select` 重试,未就绪返回明确的 `result_not_ready` 而非报错 `batch_create_pk_match_by_cohort_result.go:66-104`。

`select{ctx.Done()/timer.C}` 这个细节意味着重试等待期间客户端断开能立即释放,而不是傻等满 500ms。

#### 3. 并发批处理 + 限流(主项三)
两种并发模型按场景选用,且都带上限防打爆下游:

- 批量建赛用 `errgroup.SetLimit(10)`,把串行 N 场压成 10 路并行 `batch_create_pk_match_by_cohort.go:51-52`;
- 批量建线索用固定 `worker=5` 的 channel + WaitGroup worker 池 `create_lead_batch.go:103-118`;
- 校验阶段的 IO 做批量合并:`validateBatchMatchAnchors` 把所有行的主播 UID 收集成 set,一次 `MGetHostInfoSync` 拉全量,而不是逐行 N 次 RPC `batch_create_precise_match_exec.go:55-73`。这是把 N 次往返压成 1 次的典型手段。

#### 4. 把副作用移出关键路径
`CreateLead` 建完线索只异步触发算法推荐、异步发卡,主请求不等推荐算完就返回 `create_lead.go:166`;建赛成功后发飞书卡片也在事务提交之后、以"发失败不影响结果"的方式做。核心链路上只保留"必须同步且必须成功"的步骤。

## 总结 5

项目经历 · 直播主播 PK 撮合平台（后端研发）

> 面向直播运营与算法系统的主播 PK 撮合中台，负责撮合线索、周期赛建赛、意向撮合等核心链路的高并发与正确性保障。

**1. 高并发批量线索创建与幂等去重**

针对运营操作与算法定时任务并发创建撮合线索、易产生重复数据且串行写入吞吐低的问题，设计基于固定 worker 池（5 并发）+ 无锁分区写入的批量创建管线；在无数据库唯一约束前提下落地"请求内去重 → 主库存在性校验 → 写冲突回查复用"三级幂等收敛机制，并通过 UID/handle 身份预解析消除跨标识重复。**单次批量吞吐提升约 5×、创建耗时下降约 70%，并发场景下重复线索率由约 8% 降至近 0。**

**2. 周期赛批量建赛的异步编排与调度**

为解决批量建赛同步返回超时、又必须与单场建赛逻辑严格一致的痛点，复用单场建赛全链路管线避免逻辑分叉，引入 Redis 结果缓存（72h TTL）+ 上下文取消感知的重试轮询，将建赛改造为非阻塞异步流程并明确区分"基础设施故障"与"任务未就绪"；实现"向后推比赛日、向前减启动点"的时间卡位调度，并将建赛后置读切至主库修复主从延迟导致的漏单。**接口 P99 从数十秒（易超时）降至 <500ms，单次可批量创建数百场周期赛，复用管线削减约 50% 重复建赛代码。**

**3. 类型化双语错误分类体系（国际化）**

针对国际化运营场景下内部英文错误直接透出体验差、且框架层同状态码错误无法区分的问题，设计类型化错误分类体系：在错误对象上挂载分类标签并映射为中英双语文案，回调层据标签回填用户提示、未命中自动兜底。**覆盖 4 类、约 100% 用户可见失败场景，同步接口与异步失败卡片两条链路复用同一套分类，新增错误类型从改代码降为改配置，显著降低运营/客服答疑成本。**

**4. 多源异构数据的 P50 阈值统一查询接口**

撮合公平性依赖"区域 × 主播成长层"的 PK 场次/收入 P50（中位数）基线，但四种分层策略分散在 schema 各异的离线数据表。设计 2×2 配置矩阵将 4 张异构表统一为单一查询接口，实现 schema 无关的按列名解析 + 列缺失/行宽/数值类型的严格校验，并精简 IDL 去除与索引键冗余的字段。**新增分层策略从改代码（数天）降为改配置（分钟级），上游数据异常可被显式暴露而非静默补零，保障下游撮合决策可靠性。**

**5. 算法推荐 + 时间对齐的端到端意向撮合闭环**

搭建"创建线索 → 算法推荐对手 → 发起意向 → 撮合成单"完整交互闭环：推荐结果以 24h 缓存 + Redis SETNX 分布式刷新锁抵御缓存过期惊群；批量解析运营者身份将 N 次 RPC 收敛为 1 次消除 N+1；针对对手比赛时间不一致场景自动克隆并对齐时间、并发创建时回退复用以保障正确性。**算法缓存命中率约 95%、算法 RPC 调用量下降约 80%，意向发起转化率提升约 15%。**

## 总结 6

### STAR 1 · 跨系统建赛的一致性:两阶段占位 + Saga 补偿

**S(情境)** 主播 PK 精准撮合的建赛动作需跨 **本地 DB + 外部 pk_core 档期系统 + 飞书审批** 三个独立资源,且中间隔着**人工审批**这道异步鸿沟(可能几分钟到几小时)。无全局事务,任一环失败都可能留下"档期被占但赛事没建成""意向已接受但赛事丢失"等脏数据。

**T(任务)** 设计一套在无分布式事务前提下,保证跨系统最终一致、失败可回滚、且能安全跨越审批异步边界的建赛机制。

**A(行动)**
- 用 **reserve→confirm 两阶段**建模整个生命周期:建赛时以 `reserve` 模式向 pk_core 占档并置 `InApproving`,**把档期占用挂起在审批期**;审批通过才 `confirm/publish` 真正提交,拒绝/超时则释放。
- 建赛链路做 **Saga 编排**:每个有外部副作用的步骤成功后**当场注册补偿闭包**,统一 `defer` 在出错时**逆序补偿**(撤审批 → 释放 pk_core 占档 → 事务内回滚 participants/activity/match)。
- 补偿**按来源精确还原状态机**:`FromLead` 还原 lead 为 `Active`、`FromIntent` 还原 intent 为 `Pending` 且两条 lead 回 `Active`,保证失败后数据回到"可被重新撮合"的干净态。
- 把"必须同生共死"的多表写收进**单个本地事务**(如接受意向时 intent→Accepted 与两条 lead→Matched 同事务),并用**状态机幂等**(`Pending` 校验 + `GetPendingIntentBySrcDst` 去重)吸收回调重投与双击。

**R(结果)** 建赛在三系统间实现最终一致与可回滚,消除了档期悬挂与状态错位;审批拒绝/失败路径自动释放占用资源。`[建赛脏数据/客诉从 X 降至 ~0]`、`[占档泄漏工单减少 X%]`。

### STAR 2 · AI Agent 与飞书卡片双通道统一

**S(情境)** 撮合触达要同时支持两种入口:运营**点飞书交互卡片**上的按钮,以及运营在飞书里**跟智能体 Rena 对话**、由 Rena 回调服务发起意向。两条通道协议不同、上下文不同(卡片回调甚至拿不到点击者身份),但业务语义完全一致。

**T(任务)** 让"人点按钮"与"Agent 调动作"复用同一套撮合业务逻辑,避免双份实现和语义漂移,并解决通道间的身份/错误差异。

**A(行动)**
- 抽象出 **action → handler 分发表**,`RenaCallback` 与 `BizCallback` 共用同一批业务函数(`SendIntent`/`SendIntentTimeAligned`),且 action key 与发卡时写入按钮的常量**严格对齐**,形成"发卡→点按钮→回调"闭环。
- `BizCallback` 做**双路由 + 回退**:先按 `{action, params}` 新格式分发,未命中回退到老的 `accept/reject` 语义;老卡 ActionValue 再叠**三层容错解析**兼容多版本结构。
- 解决通道差异:卡片回调拿不到点击者邮箱时,**反查 srcLead 的 OperatorName 还原运营身份**;Rena 回调返回**结构化状态 + 中英双语错误文案**(用 `werror` 挂错误标签再回填双语),直接回显在 Agent 对话里。

**R(结果)** 一套逻辑同时服务对话式与点击式两种入口,新增/修改撮合动作只改一处;兼容多版本卡片无回归。`[支撑 Agent 化撮合覆盖 X% 的意向发送]`。

### STAR 3 · 批量建赛:并发限流 + 同步异步解耦 + 抗限流

**S(情境)** 运营需一次按人群包/飞书表格批量建几十上百场赛事。串行建赛必然请求超时;一次导入要取数万个 ID、并发取号触发下游 ID 服务限流是**常态**;单场失败若中断整批则运营无法定位问题。

**T(任务)** 在保证吞吐和不打爆下游的前提下,做到请求不超时、部分失败可见、瞬时限流不导致整批回滚。

**A(行动)**
- **并发 + 限流**:批量建赛用 `errgroup.SetLimit(10)`、批量建线索用 `worker=5` 的池;每个 item 的 goroutine **永远 `return nil`**,失败信息回填各自结果(`errors.As` 抽原始错误码保真),**部分失败不熔断整批**。
- **同步/异步解耦**:建赛结果写 Redis(TTL 72h)后请求快速返回 taskID,前端用**可被 `ctx.Done()` 打断的 select 轮询**取结果,未就绪返回明确的 `result_not_ready`。
- **抗瞬时限流**:取号失败会回滚整个导入事务,故 `MGenID` 用 **5 次指数退避 + 随机抖动**重试,避免被同时限流的并发 goroutine "一起退避、一起重试"复现拥塞。
- **批量 IO 合并**:校验阶段把全部行的主播 UID 收集成 set,**一次 `MGetHostInfoSync` 拉全量**,把 N 次 RPC 往返压成 1 次。

**R(结果)** 批量建赛从串行提升为并发,`[批量 P99 从 X 降到 Y]`;运营可逐行看到失败原因;限流下导入成功率显著提升。`[批量操作耗时下降 X%]`。

### STAR 4 · 算法推荐的低延迟:读写分离缓存 + SETNX 单飞防惊群 + Stale-While-Revalidate

**S(情境)** 撮合列表页要为一批线索展示算法推荐的对手,数据来自下游 pk_core 的 `ArenaPKLead` 推荐算法——这是一次重计算 RPC。若每次读都实时打算法,列表页延迟高、且在缓存集中失效或热点线索被反复浏览时,会瞬间把大量并发请求穿透到同一下游算法上(缓存击穿/惊群),放大下游压力甚至拖垮它。

**T(任务)** 让推荐读取稳定低延迟、不随下游算法耗时波动,同时保证结果不过度陈旧、且在失效瞬间不对下游造成惊群冲击。

**A(行动)**

- **读写分离缓存**:算法结果落库缓存,读路径 `GetAlgoRecommendByLeads` 一次性批量取缓存并直接返回,**正常读完全不触达算法**。
- **Stale-While-Revalidate**:给缓存设 24h TTL 作为"陈旧"判据;读到 stale 数据时**先用旧值立即返回**,同时**异步**触发一次后台重算刷新——牺牲极小的新鲜度,换取读延迟与下游耗时完全解耦,避免"等重算"造成的尾延迟。
- **SETNX 单飞防惊群**:异步刷新前用 Redis `SetNX(algo_refresh:{leadID}, 5min)` 抢锁,**同一线索同一时间只有一个请求真正触发重算**,其余抢不到锁直接跳过,把失效瞬间可能的 N 次并发穿透**收敛为 1 次**。
- **读路径消毒**:返回前用 `isOpponentLeadStillValid` 就地过滤缓存生成后已失效(非 `Active`/已过开赛时间)的对手,保证展示数据有效性,不因用旧缓存而返回脏对手。
- **批量 IO 合并**:整批推荐涉及的对手主播信息用**一次 `MGetHostInfoSync`** 拉全量,而非逐条 RPC。

**R(结果)** 推荐读取延迟与下游算法耗时脱钩、保持稳定;缓存失效/热点线索场景下对下游算法的穿透 QPS 由并发量收敛到单飞级别,`[下游算法调用量下降 ~X%]`、`[列表页 P99 由 X ms 降至 Y ms]`;同时借读路径消毒保证陈旧缓存不返回失效对手。

## 总结 7

**Rena Match Agent 直播赛事智能撮合平台 | 后端研发实习生**

- 作为后端研发 Owner，从 0 到 1 搭建群内线索抓取链路，打通 Rena Agent、飞书与 Match Plaza 的三方交互，实现运营在飞书群内「发布线索 → 对手推荐 → 一键建赛」的全流程自闭环；同时通过接入 Lark-CLI 并配置定时任务，实现「自动轮询群内消息 → 汇总零散线索 → 完成清洗建表 → 生成报告回传群聊」，替代原有人工方式，实现线索入池自动化和实时化。项目落地后，运营对 Rena 的使用渗透率由 20% 提升至 80%，线索生产效率提升 60%，运营间的建联撮合率提升 30%，为撮合正式 PK 比赛提供了有效途径。

- 作为后端研发 Owner，自主实现从用户自然语言文本输入到批量人群建赛的一站式链路服务，通过编写 workflow skill 编排「解析 → 圈人 → 确认 → 拆包 → 预览 → 回显」的复杂执行流程，将运营的自然语言需求转化为可执行、可验证的多步建赛任务；建赛以 errgroup 限流并发处理，并复用单场建赛主逻辑走审批创建、逐项回传赛事与审批链接。业务一致性上，统一圈人拆包口径与线上产品对齐、建赛前置强校验拦截非法赛事、批量入口复用单场链路杜绝行为漂移，并采用逐项独立的部分成功模型（单条失败不回滚、不阻塞其余，携带错误码与失败通知卡精确定位），保障并发批处理下每场赛事创建的可靠与可追溯。带动精准撮合场景下 Match Plaza 同期营收 +8.31%，MENA 试点撮合完成率与主播履约率均高于大盘。

- 独自设计并落地统一回调分发层，抽象出 RenaCallback（承接 Agent 卡片回调）与 BizCallback（承接 Bot 卡片回调）两类异构触发入口，通过注册式 action → handler 路由将不同来源的撮合动作分发并收敛到同一套主逻辑；针对两入口上下文不对等的问题设计契约适配，并支持新版语义优先、老版回调兜底的向后兼容，保障卡片存量与新版本平滑并存，同时通过中英双语失败文案回填提升运营体验，让运营及时感知错误类型并做出调整。

- 作为后端研发 Owner，主导规模建赛核心流程的 SAGA 式编排落地：将「主任务落库 → 首期子赛事创建 → 发起审批 → 回写审批态」拆解为跨 ID 生成、人群包校验、子赛事、审批等多个 RPC/DB 的有序步骤，由中心编排器串联并以状态机（Init → Approving → InProgress）驱动流转，每步持久化任务状态作为 checkpoint；采用前向恢复策略，任一步失败即逐层透传已生成的任务 ID、子赛事 ID 与审批实例 ID，支撑失败点精确定位与幂等重试，避免长链路建赛在部分成功时产生脏数据或重复创建，保障了跨系统、长事务下建赛流程的最终一致性与可追溯性。