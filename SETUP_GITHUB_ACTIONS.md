# GitHub Actions 手动设置指南

## 重要说明
由于OAuth权限限制，GitHub Secrets和Workflow文件需要你手动添加。

## 第一步：添加GitHub Secrets

1. 访问你的仓库：`https://github.com/hugetiny/Edu-Mail-Generator`
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 添加以下secret：
   - **Name**: `EDU_EMAIL`
   - **Value**: 你的邮箱地址（**重要：不要使用hugetiny@hotmail.com，使用你自己的邮箱**）

## 第二步：创建GitHub Actions Workflow

1. 在你的仓库中，点击 **Actions** 标签
2. 点击 **New workflow**
3. 选择 **set up a workflow yourself**
4. 将文件命名为 `edu-mail-generator.yml`
5. 复制以下YAML内容：

```yaml
name: Edu Mail Generator

on:
  workflow_dispatch:
    inputs:
      college_id:
        description: 'College ID (1-5)'
        required: true
        default: '1'
        type: choice
        options:
        - '1'
        - '2'
        - '3'
        - '4'
        - '5'

jobs:
  generate-edu-mail:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y wget gnupg unzip curl xvfb
    
    - name: Install Google Chrome
      run: |
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Create configuration
      run: |
        echo "chrome_undetected" > prefBrowser.txt
        cat > config.json << EOF
        {
          "browser": "chrome_undetected",
          "headless": true,
          "timeout": 60,
          "retry_attempts": 3,
          "delay_between_actions": 0.7,
          "captcha_timeout": 300,
          "output_file": "generated_accounts.txt",
          "log_level": "INFO"
        }
        EOF
    
    - name: Run Edu Mail Generator
      env:
        EDU_EMAIL: ${{ secrets.EDU_EMAIL }}
        DISPLAY: :99
      run: |
        Xvfb :99 -screen 0 1920x1080x24 &
        sleep 3
        python edu_mail_generator.py
    
    - name: Upload generated accounts
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: generated-accounts
        path: |
          generated_accounts.txt
          edu_generator.log
        retention-days: 30
```

6. 点击 **Commit changes**

## 第三步：运行Workflow

1. 进入 **Actions** 标签
2. 选择 **Edu Mail Generator** workflow
3. 点击 **Run workflow**
4. 选择学院ID (1-5)
5. 点击 **Run workflow** 开始执行

## 学院列表

1. **MSJC College** (ID: 1)
2. **Contra Costa College** (ID: 2)  
3. **City College** (ID: 3)
4. **Sacramento College** (ID: 4)
5. **Mt San Antonio** (ID: 5)

## 本地运行方式

如果你想在Windows本地运行：

### 方法1：使用启动脚本
```cmd
# Windows
run_windows.bat

# Linux/Mac
./run_unix.sh
```

### 方法2：手动运行
```cmd
# 1. 安装依赖
python setup_modern.py

# 2. 配置邮箱
copy .env.example .env
# 编辑 .env 文件，设置你的邮箱

# 3. 运行生成器
python edu_mail_generator.py
```

## 注意事项

- ⚠️ **绝对不要在代码中硬编码你的邮箱地址**
- ✅ 使用GitHub Secrets或.env文件管理敏感信息
- 📁 生成的账户信息会保存在 `generated_accounts.txt`
- 🔄 GitHub Actions执行结果可在Artifacts中下载
- ⏰ Artifacts保留30天后自动删除
