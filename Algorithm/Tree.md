# Tree



   * [最近公共祖先](#最近公共祖先)
   * [原地翻转](#原地翻转)



## 最近公共祖先

```text
给定一棵二叉树，以及树中的两个不同节点 p 和 q，请你返回它们的最近公共祖先（Lowest Common Ancestor, LCA），定义为在树中同时拥有 p 和 q 作为后代的最深的那个节点。注意：一个节点也可以是它自己的祖先。
```

由于二叉树的每个节点最多只有左右两个子节点，因此 p 和 q 的相对位置只可能出现两种情况：1️⃣ 要么一个在祖先的左边，要么一个在祖先的右边；2️⃣ 要么一个就是祖先，要么一个在祖先的左边或右边

实际上，我们不需要关心 p 是左边的还是 q 是左边的，也就是说 p 和 q 的顺序不存在干扰，那么这两种情况都可以通过自底向上的递归统一解决，每个节点在递归中都只做一件事，即**向父节点上报自己找到的可能是 LCA 的节点**

- 如果自己是空，那么就上报空（递归终点）
- 如果自己是 p/q，那么就上报自己（递归终点）
- 如果左子节点和右子节点上报都不为空，那么就上报自己
- 如果左子节点和右子节点上报有一个为空，那么就上报非空的那个
- 如果左子节点和右子节点上报都为空，那么就上报空

```java
class Solution {
    public TreeNode LCA(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = LCA(root.left, p, q);
        TreeNode right = LCA(root.right, p , q);

        if (left != null && right != null) {
            return root;
        }

        return left != null ? left : right;
    }
}
```



## 原地翻转

```text
给你一棵二叉树的根节点 root，请你原地翻转这棵二叉树，并返回它的根节点。
    4									4
   / \							 / \
  2   7			➡️			7   2
 / \ / \					 / \ / \
1  3 6  9					9  6 3  1
```

本质是右节点 = 左节点，左节点 = 右节点，但是必须先把下面构造好，所以采用递归的方式，只有到叶子节点才结束递归

需要注意的是，不能直接 `root.left = invertTree(root.right); root.right = invertTree(root.left);`，因此第二步会使用第一步结束后翻转的节点，但实际上我们应该使用的是原先的节点，所以应该先得到节点，再交换指针

```java
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;

        TreeNode left = invertTree(root.left);
        TreeNode right = invertTree(root.right);
      
        root.left = right;
        root.right = left;
      
        return root;
    }
}
```