# 吉利元亨 KUEI TEA｜網站使用說明

這是一個**純靜態網站**：HTML 負責內容、CSS 負責外觀、JavaScript 負責互動。
目前不需要 npm、Node.js、React、Vite 或資料庫，直接就能預覽與發布。

## 1. 先看網站（最簡單）

下載或複製此專案後，開啟根目錄的 `index.html`，即可查看首頁。
若需模擬正式網站的網址行為，可在專案資料夾開啟終端機，執行：

```sh
# Mac / Linux
python3 -m http.server 8000

# Windows
py -m http.server 8000
```

然後用瀏覽器開啟 http://localhost:8000/ 。按 Ctrl+C 可以結束伺服器。

> 為何使用這個方法：Python 內建簡易網頁伺服器，避免為一頁式展示網站增加安裝與編譯流程。若電腦沒有 Python，可先直接開啟 index.html。

## 2. 更改網站內容

| 想修改什麼 | 修改哪個檔案 |
|---|---|
| 首頁文字、圖片、區塊、導覽 | `index.html` |
| 全站排版、字型、顏色 | `assets/css/main.css` |
| 首頁動畫 | `index.html` 末端的腳本 |
| 互動、畫面大小切換、相簿 | `assets/js/main.js` |
| 產品列表 | `products/index.html` |
| 第一個茶品介紹 | `products/p1.html` |
| 品牌檔案 | `archive/index.html` |
| 合作資訊 | `partners/index.html` |
| 品牌照片 | `images/` |

**重要：** 目前產品名稱、年份、產地及文字有草稿示例；發布前應逐一與品牌主理人確認，避免將示例當成正式產品資料。

## 3. 發布網站（GitHub Pages）

1. 在 GitHub 開啟此 repository → **Settings → Pages**。
2. **Build and deployment** 選 `Deploy from a branch`。
3. Branch 選 `main`、資料夾選 `/(root)`，儲存。
4. 等待 GitHub 顯示發布成功，再使用 **Visit site** 開啟網站。
5. 若修改是在 Pull Request（PR）分支，需先測試並合併到 `main`，才會影響正式網站。

若沿用此專案名稱，GitHub Pages 的預設專案網址通常是：
https://kuei0857.github.io/kueitea-site/

**注意：** 以上為 GitHub Pages 的預期網址，是否已啟用及自訂網域仍需在 Settings → Pages 確認。

## 4. 每次修改後的檢查

執行：

```sh
python3 scripts/check_links.py
```

這個檢查會確認 HTML 裡的本地連結、圖片、CSS、JS 路徑是否存在，並檢查頁面錨點。
如果路徑寫錯，會列出檔案及行號。**它只能檢查靜態連結，不能代替手機與桌面瀏覽器實際測試。**

## 5. 為什麼現在保留原架構？

- **不用編譯**：一頁式展示網站先維持輕量。
- **相對路徑**：相同程式可在本機、專案子路徑與自訂網域使用。
- **留下修改原因**：重要邏輯在程式碼旁加中文註解，較完整的紀錄放在 `docs/CHANGELOG.md`。
- **循序擴充**：未來有沖泡紀錄、會員或大量動態內容時，再決定是否需要新框架與後端。

程式碼的既有 HTML5 UP Strata 模板及授權註記予以保留。