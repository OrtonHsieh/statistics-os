# Statistics OS · Exam Edition

政大 MBA「商業數量方法」Chapters 12–18 的互動式考試學習網站。純 HTML、CSS、Vanilla JavaScript，無登入、無後端，GitHub Pages 可直接部署。

## 專案結構

```text
statistics OS/
├── index.html       # 頁面結構
├── styles.css       # Material / Google Docs 風格與 responsive UI
├── data.js          # 主題、題目、答案、來源與教戰資料
├── question-bank.js # 由 7 份 PDF 產生的 684 題原文題庫
├── answers.js       # 已獨立驗算的答案覆寫層
├── app.js           # 搜尋、作答、錯題、收藏、模擬考與 localStorage
├── scripts/
│   └── build_question_bank.py # 從 PDF 重建原題與題號
├── sources/          # 原始 Chapter PDF，可由每題直接開到對應頁
├── ANALYSIS.md      # Syllabus、題庫矩陣、風險與內容範圍
└── README.md
```

## 如何啟動

最簡單：直接雙擊 `index.html`。

若瀏覽器限制本機檔案，可在本資料夾執行：

```bash
python3 -m http.server 8000
```

再開啟 `http://localhost:8000`。

## 如何新增考題

原始題庫由 `scripts/build_question_bank.py` 產生。新增 PDF 時先在腳本的 `FILES` 加入來源，再重新執行腳本。人工驗證答案則加在 `answers.js`，不要直接改 generated file。

不要大段複製受版權保護的題庫文字；應摘要或改寫，並保留 `source` 以便回查。

## 如何新增主題

在 `data.js` 的 `TOPICS` 陣列新增物件。主題 id 必須與相關 question 的 `topic` 完全相同。至少補齊定位、商業問題、條件、公式、Excel、關鍵字、陷阱與 mini quiz。

## 如何修改答案

找到 `QUESTIONS` 中對應 id：

- `answer` 是正確選項的零起算位置：A=0、B=1、C=2、D=3。
- 同時更新 `steps`、`statConclusion`、`businessConclusion`。
- 修改後重新手算，並以 Excel 函數交叉驗證。

## 如何重設進度

網站內進入 **Settings → 清除所有資料**。這會刪除瀏覽器中 `statisticsOS.exam.v2` 的 localStorage。

## 如何部署

### GitHub Pages

1. 將所有檔案放在 repository 的 `main` branch 根目錄。
2. Settings → Pages。
3. Source 選 `Deploy from a branch`。
4. 選 `main` 與 `/ (root)`。
5. 儲存後等待 Pages 發布。

之後只要更新並 commit/push 檔案，Pages 會自動重新部署。

### Vercel / Netlify

匯入 GitHub repository；這是純靜態網站，不需要 build command，publish directory 使用 repository root（`.`）。

## 學習資料

進度、答案、錯題、收藏、模擬考紀錄、考試日期與主題全部存在 localStorage。換瀏覽器或清除網站資料後不會自動同步；可在 Settings 匯出 JSON 備份。

## 內容限制

提供的 Chapter Q-set 是按章題庫，不是帶年份與配分的歷屆考卷。Practice Center 已完整重建 684 題原文、Exhibit、章節、題型、題號與 PDF 頁碼。答案採獨立 audit layer；只有重新計算或定義核對完成的題目會顯示「已驗證」，其餘不顯示猜測答案。
