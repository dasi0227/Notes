'use strict'

const { stripHTML, escapeHTML, prettyUrls } = require('hexo-util')
const crypto = require('crypto')

hexo.extend.helper.register('page_description', function () {
  const { config, page } = this
  let description = page.description || page.content || page.title || config.description

  if (description) {
    description = escapeHTML(stripHTML(description).substring(0,250)
      .trim()
    ).replace(/\n/g, ' ')
    return description
  }
})

hexo.extend.helper.register('cloudTags', function(options = {}) {
  const env = this
  // 设置标签排序：根据文章数目'length'从小到大排序，然后再翻转实现从大到小排序
  let source = options.source
  source = source.sort('length').reverse()
  // 设置标签上限：显示全部标签
  const limit = options.limit
  if (limit > 0) source = source.limit(limit)
  // 设置标签格式
  let result = ''
  source.forEach(tag => {
    // 随机取(100,100,100)~(255,255,255)的鲜艳颜色，为了更好地显示
    const color = 'rgb(' + Math.floor(Math.random()*156+100) + ', ' + Math.floor(Math.random()*156+100) + ', ' + Math.floor(Math.random()*156+100) + ')'
    // 增加 (${tag.length})内容，显示文章数目
    result += `<a href="${env.url_for(tag.path)}" style="color: ${color}">${tag.name} (${tag.length})</a>`
  })
  return result
})

hexo.extend.helper.register('urlNoIndex', function (url = null, trailingIndex = false, trailingHtml = false) {
  return prettyUrls(url || this.url, { trailing_index: trailingIndex, trailing_html: trailingHtml })
})

hexo.extend.helper.register('md5', function (path) {
  return crypto.createHash('md5').update(decodeURI(this.url_for(path))).digest('hex')
})

hexo.extend.helper.register('injectHtml', function (data) {
  if (!data) return ''
  return data.join('')
})

hexo.extend.helper.register('findArchivesTitle', function (page, menu, date) {
  if (page.year) {
    const dateStr = page.month ? `${page.year}-${page.month}` : `${page.year}`
    const dateFormat = page.month ? hexo.theme.config.aside.card_archives.format : 'YYYY'
    return date(dateStr, dateFormat)
  }

  const defaultTitle = this._p('page.archives')
  if (!menu) return defaultTitle

  const loop = (m) => {
    for (const key in m) {
      if (typeof m[key] === 'object') {
        loop(m[key])
      }

      if (/\/archives\//.test(m[key])) {
        return key
      }
    }
  }

  return loop(menu) || defaultTitle
})

hexo.extend.helper.register('isImgOrUrl', function (path) {
  const imgTestReg = /\.(png|jpe?g|gif|svg|webp)(\?.*)?$/i
  return path.indexOf('//') !== -1 || imgTestReg.test(path)
})
