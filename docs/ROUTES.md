# 路由與頁面設計 (API & Route Design)

本文件定義了選課交換平台的 URL 結構、HTTP 方法對應的處理邏輯，以及渲染畫面的 Jinja2 模板清單。

## 1. 路由總覽

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁 / 熱門看板 | GET | `/` | `index.html` | 顯示系統簡介與目前熱門課程排行榜 |
| 登入頁面 | GET, POST | `/login` | `login.html` | 顯示登入表單與處理登入驗證 |
| 註冊頁面 | GET, POST | `/register` | `register.html` | 顯示註冊表單與處理註冊邏輯 (限 .edu.tw) |
| 登出 | GET | `/logout` | — | 清除 Session 並重導向至首頁 |
| 許願清單頁面 | GET | `/wishlist` | `wishlist.html` | 列出使用者目前所有的持有與目標課程 |
| 新增許願 | POST | `/wishlist/add` | — | 接收表單新增願望，存入資料庫後重導向 `/wishlist` |
| 刪除許願 | POST | `/wishlist/<id>/delete` | — | 刪除單筆願望，重導向 `/wishlist` |
| 評價使用者 | POST | `/matches/<id>/rate` | — | 在完成交易後對換課對象給予評價，更新信用分數 |
| 媒合列表 | GET | `/matches` | `matches.html` | 顯示目前所有配對成功的組合列表 |
| 進入聊天室 | GET | `/chat/<match_id>` | `chat.html` | 進入特定配對的匿名聊天室 |
| 發送訊息 | POST | `/chat/<match_id>/send` | — | 接收聊天訊息並存入資料庫，支援 AJAX 或表單重導向 |

## 2. 路由詳細說明

### Blueprint: `main` (`app/routes/main.py`)
- **`GET /`**
  - **輸入**: 無
  - **處理邏輯**: 查詢 `courses` 與 `wishlists` 計算熱門需求課程與熱門釋出課程。
  - **輸出**: 渲染 `index.html`

### Blueprint: `auth` (`app/routes/auth.py`)
- **`GET, POST /login`**
  - **輸入**: 表單 (email, password)
  - **處理邏輯**: 比對密碼，成功則設定 `session['user_id']`。
  - **輸出**: 成功則重導向 `/wishlist`，失敗則帶錯誤訊息重新渲染 `login.html`。
- **`GET, POST /register`**
  - **輸入**: 表單 (email, password)
  - **處理邏輯**: 驗證信箱後綴，建立 `User`，設定 session。
  - **輸出**: 成功重導向 `/wishlist`，失敗渲染 `register.html`。
- **`GET /logout`**
  - **輸入**: 無
  - **處理邏輯**: 清除 session。
  - **輸出**: 重導向 `/`

### Blueprint: `course` (`app/routes/course.py`)
- **`GET /wishlist`**
  - **輸入**: Session 中 `user_id`
  - **處理邏輯**: 查詢使用者的 `wishlists` 並關聯 `courses` 資料。
  - **輸出**: 渲染 `wishlist.html`
- **`POST /wishlist/add`**
  - **輸入**: 表單 (held_course_id, target_course_id)
  - **處理邏輯**: 檢查課程是否存在，建立願望，並觸發媒合檢查。
  - **輸出**: 重導向 `/wishlist`
- **`POST /wishlist/<id>/delete`**
  - **輸入**: URL 參數 `id`
  - **處理邏輯**: 驗證權限後刪除。
  - **輸出**: 重導向 `/wishlist`

### Blueprint: `chat` (`app/routes/chat.py`)
- **`GET /matches`**
  - **輸入**: Session `user_id`
  - **處理邏輯**: 查詢與此使用者相關的所有 `matches`。
  - **輸出**: 渲染 `matches.html`
- **`GET /chat/<match_id>`**
  - **輸入**: URL 參數 `match_id`
  - **處理邏輯**: 驗證使用者是否為配對的其中一方，載入 `chat_messages`。
  - **輸出**: 渲染 `chat.html`
- **`POST /chat/<match_id>/send`**
  - **輸入**: 表單 (content)
  - **處理邏輯**: 儲存訊息至 `chat_messages`。
  - **輸出**: 重導向 `/chat/<match_id>` 或回傳 JSON (若前端用 AJAX)。

## 3. Jinja2 模板清單

所有模板皆置於 `app/templates/` 目錄下：

1. `base.html`：母版，包含 Navbar、Footer 與共用 CSS/JS 引用。
2. `index.html`：繼承 `base.html`，首頁與熱門看板。
3. `login.html`：繼承 `base.html`，登入畫面。
4. `register.html`：繼承 `base.html`，註冊畫面。
5. `wishlist.html`：繼承 `base.html`，個人願望清單管理畫面。
6. `matches.html`：繼承 `base.html`，配對成功列表。
7. `chat.html`：繼承 `base.html`，匿名聊天室畫面。
