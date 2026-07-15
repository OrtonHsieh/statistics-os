# Phase 1：檔案分析

## 1. Syllabus 主題整理

| 教學順序 | Chapter | 主題 | 課程活動 | 期末範圍 |
|---:|---:|---|---|---|
| 1 | 12 | Chi-square Test | 第一次作業 | 是 |
| 2 | 13 | ANOVA | 第一次案例分析 | 是 |
| 3 | 14 | Regression I | 第二次作業 | 是 |
| 4 | 15 | Regression II | 第二次案例分析 | 是 |
| 5 | 16 | Regression III / Model Construction | 第三次作業 | 是 |
| 6 | 17 | Time Series & Forecasting | 第三次案例分析 | 是 |
| 7 | 18 | Nonparametric Methods | 第四次作業 | 是 |

期末明列 Chapters 12–18。Chapter 21 Quality Control 雖在課程週次中，但不在 syllabus 的 final exam 範圍。本課重點是 model、business interpretation、case/data analysis 與 statistical software，不只是手算。

可能需要 Excel：Chi-square p-value、ANOVA/Regression output、forecasting spreadsheet、rank 計算。可能手算：expected counts、df、ANOVA table 缺格、slope/R²、t/F、weighted moving average、sign/rank test。幾乎每一章都要求把統計結論翻譯成管理語言。

## 2. 題庫清單與內容分布

| 檔案 | 選擇題 | Problems | 主要題型 |
|---|---:|---:|---|
| Chapter 12 | 47 | 35 | GOF、independence、Poisson/Normal fit、E、df、p-value |
| Chapter 13 | 68 | 47 | One-way ANOVA、ANOVA table、LSD、block、factorial |
| Chapter 14 | 113 | 33 | Least squares、r、R²、t/F、CI/PI、Excel output |
| Chapter 15 | 約 85 | 30 | Multiple regression、coefficient t、overall F、adjusted R² |
| Chapter 16 | 48 | 29 | Partial F、quadratic、interaction、dummy、selection、DW |
| Chapter 17 | 37 | 31 | MA/WMA、exponential smoothing、trend、seasonality、MAE/MSE |
| Chapter 18 | 53 | 28 | Sign、Mann–Whitney、Wilcoxon、Spearman |

這批 PDF 沒有年度、配分、建議時間與官方答案，因此不能建立真正的「年度歷屆試卷模式」。網站以 `source filename + exhibit/problem number` 追溯。

## 3. 考試重點矩陣

題庫在每章的題數不同，不等於實際出題頻率。以下 priority 綜合 syllabus、作業、題型重複性與解題鏈核心性。

| 主題 | 題庫量 | 常見形式 | 難度 | 必考程度 |
|---|---:|---|---|---|
| Chi-square | 82 | 選檢定、算 E/χ²/df、結論 | 中 | S |
| ANOVA | 115 | 完整表、F、LSD、block | 中高 | S |
| Simple Regression | 146 | 建式、r/R²、t/F、輸出 | 中高 | S |
| Multiple Regression | 115 | 係數解讀、個別 t、整體 F | 高 | S |
| Model Construction | 77 | 新增變數、dummy、interaction、DW | 高 | A |
| Forecasting | 68 | WMA、smoothing、error、trend | 中 | A |
| Nonparametric | 81 | 選 rank test、手算 statistic | 中 | A |

## 4. 老師／題庫常見判斷模式

1. 先辨識資料型態與研究設計，再選方法。
2. 固定要求 H₀/H₁、α、test statistic、critical/p-value、decision。
3. Chi-square 反覆測 expected count、自由度與 GOF/independence 分流。
4. ANOVA 反覆要求補表；顯著後用 Fisher LSD。
5. Regression 同時考整體 F 與個別 t，並要求係數、R² 的管理解讀。
6. Chapter 16 強調模型不是 R² 越高越好；要做 nested F 與 residual diagnostics。
7. Forecasting 反覆考逐期更新，最容易發生 time index 錯位。
8. Nonparametric 的核心是 paired vs independent，以及 ranks/signs 的資訊差異。

## 5. 網站資訊架構

```text
Dashboard
├── Countdown / Recommendation / Metrics
├── Priority map
└── Source-volume chart
Knowledge System
├── Interactive decision tree
├── Topic position / business question / conditions
└── Formula / Excel / trap / mini quiz
Practice Center
├── Filters / single-question mode
├── answer → grading → full explanation
├── wrong book / favorites
└── timed simulation
Exam Strategy
├── six-step recognition algorithm
├── method table / answer template
└── 7-day / 3-day / 1-day / 60-minute sprint
Settings
├── Light/Dark
├── export progress
└── reset localStorage
```

## 6. 資料缺漏與風險

- 沒有按年度的正式歷屆試卷，不能可靠計算「老師歷年出題頻率」。
- 沒有官方解答；所有網站答案都需自行重算並標記信心。
- 部分 PDF 公式在文字抽取時遺失，需回看原頁；資訊不足的題目不可補造數字。
- Q-set 有 Cengage 著作權聲明，不宜把整份題庫逐字發布到公開 GitHub Pages。Practice Center 使用摘要／改寫並保留 reference。
- Practice Center 已重建全部 684 個題項並完成全庫稽核：682 題答案已獨立驗證，2 題確認為題源錯誤，0 題待驗證。題源錯誤不補造答案：Chapter 16 MC 8 缺少正確選項 Durbin–Watson；Chapter 18 Problem 19 的樣本數 80 與分類合計 85 互相矛盾。
- 2026-07-15 audit：451 題選擇題中，450 題已逐題驗證；Chapter 16 MC 8 因正確的 Durbin-Watson test 不在 A-D 選項內，標記為 source error。Chapter 12–16 的計算題已完成 178/178；全部計算題目前 178/233 verified、55 pending。全題庫狀態為 628 verified、55 pending、1 source error。
- Chapter 13 題源稽核另發現舊解析器會把不等樣本表中「單獨一行的觀察值」誤刪為頁碼。解析器已修正，跨頁／尾端觀察值已依 PDF 視覺核對後重新分組顯示，相關 ANOVA 答案也以完整樣本重算。
- Chapter 14 的 PDF 文字層會遺失 Ŷ、x̄、ȳ 與 Σ 等公式符號；網站題目已依原頁補回，避免只剩空括號而無法辨識公式。
- Chapter 15 有 7 題的完整迴歸式與 dummy 變數定義未進入 PDF 文字層；已逐頁視覺核對並補回。相關預測特別依 0/1 dummy 定義計算，沒有把廣告次數或車庫數量誤當 dummy 值。
- Chapter 16 遺失的線性／二次模型式、縮減／完整巢狀模型式與 dummy 係數已依原頁補回。新增變數題均以完整模型的 error df 計算 partial F；接近 5% 邊界的題目保留精確 p-value，不以四捨五入猜結論。
