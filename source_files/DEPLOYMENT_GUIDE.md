# 🌐 网站部署指南 - 让你的AI网站在互联网上公开访问

本文档提供了多种将你的 `ai_basics.html` 网站部署到互联网的方法。

---

## 🎯 方法一：GitHub Pages（推荐，免费！）

这是最简单、免费的方法，适合静态网站。

### 步骤：

1. **确保文件已推送到GitHub**
   - 你的 `ai_basics.html` 应该已经在 GitHub 仓库中了

2. **重命名文件（可选但推荐）**
   ```bash
   # 将 ai_basics.html 重命名为 index.html（GitHub Pages默认寻找的文件）
   cp ai_basics.html index.html
   git add index.html
   git commit -m "Add index.html for GitHub Pages"
   git push
   ```

3. **在GitHub上启用GitHub Pages**
   - 打开你的GitHub仓库：https://github.com/Galaxy1203/wsl
   - 点击仓库页面的 **Settings**（设置）
   - 在左侧菜单找到 **Pages**（页面）
   - 在 **Build and deployment** 部分：
     - Source（源）选择：**Deploy from a branch**（从分支部署）
     - Branch（分支）选择：**main** 分支
     - 文件夹选择：**/ (root)**
   - 点击 **Save**

4. **等待部署完成**
   - 通常需要1-2分钟
   - 刷新 GitHub Pages 页面，你会看到一个绿色的提示：
     "Your site is live at https://galaxy1203.github.io/wsl/"

5. **访问你的网站**
   - 网址格式：`https://你的用户名.github.io/仓库名/`
   - 你的网站地址应该是：`https://galaxy1203.github.io/wsl/`

---

## 🎯 方法二：Vercel（免费，速度快）

Vercel 提供免费的静态网站托管，部署非常简单。

### 步骤：

1. **访问 Vercel**
   - 打开：https://vercel.com
   - 使用 GitHub 账号登录

2. **导入仓库**
   - 点击 "New Project"
   - 选择你的 `wsl` 仓库
   - 点击 "Import"

3. **配置项目**
   - Project Name：输入项目名称（如 `ai-basics`）
   - Framework Preset：选择 `Other`
   - Root Directory：保持默认
   - Output Directory：留空
   - Install Command：留空

4. **确保有 index.html**
   - 在项目根目录创建 `index.html`（可以复制 `ai_basics.html`）

5. **部署**
   - 点击 "Deploy"
   - 等待1-2分钟
   - 完成后会给你一个类似 `https://ai-basics-xxx.vercel.app` 的网址

---

## 🎯 方法三：Netlify（免费，拖拽即可）

Netlify 也是一个很棒的选择，甚至可以直接拖拽文件部署。

### 方式A：通过Git部署
1. 访问 https://netlify.com
2. 用 GitHub 登录
3. 点击 "New site from Git"
4. 选择 GitHub，选择你的仓库
5. 点击 "Deploy site"

### 方式B：拖拽部署（最简单）
1. 在本地创建一个文件夹，把 `ai_basics.html` 改名为 `index.html` 放进去
2. 访问 https://app.netlify.com/drop
3. 直接把文件夹拖进去
4. 几秒钟后就有网址了！

---

## 🎯 方法四：Cloudflare Pages（免费，全球CDN）

Cloudflare Pages 提供免费的全球CDN加速，速度非常快。

### 步骤：
1. 访问 https://pages.cloudflare.com
2. 注册/登录 Cloudflare 账号
3. 点击 "Create a project"
4. 选择 "Connect to Git"
5. 选择你的 GitHub 仓库
6. 配置部署设置：
   - Project name：输入项目名
   - Production branch：main
   - Framework preset：None
7. 点击 "Save and Deploy"

---

## 📋 对比表

| 平台 | 免费额度 | 自定义域名 | SSL证书 | 部署速度 | 推荐度 |
|------|---------|-----------|---------|---------|--------|
| GitHub Pages | 无限 | ✓ | ✓ | 中等 | ⭐⭐⭐⭐⭐ |
| Vercel | 无限 | ✓ | ✓ | 快 | ⭐⭐⭐⭐⭐ |
| Netlify | 100GB/月 | ✓ | ✓ | 快 | ⭐⭐⭐⭐ |
| Cloudflare Pages | 无限 | ✓ | ✓ | 极快 | ⭐⭐⭐⭐⭐ |

---

## 💡 额外建议

### 1. 创建 index.html
无论使用哪个平台，建议将 `ai_basics.html` 复制为 `index.html`，这样访问根域名时就能直接打开：

```bash
cp ai_basics.html index.html
git add index.html
git commit -m "Add index.html"
git push
```

### 2. 想同时保留两个文件？
可以！创建一个简单的 `index.html` 作为入口，提供链接到两个页面：

```html
<!DOCTYPE html>
<html>
<head>
    <title>我的项目</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        .link-btn {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>🚀 欢迎来到我的项目</h1>
    <p>选择一个页面访问：</p>
    <br>
    <a href="ai_basics.html" class="link-btn">🧠 AI基础概念</a>
    <a href="crocodile_run.html" class="link-btn">🐊 小鳄鱼跑酷</a>
</body>
</html>
```

---

## 🆘 需要帮助？

如果在部署过程中遇到问题，可以：
1. 检查各平台的官方文档
2. 确保你的 `index.html` 在仓库根目录
3. 等待几分钟让部署生效

祝你部署顺利！🎉