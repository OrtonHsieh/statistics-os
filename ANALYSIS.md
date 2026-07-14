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
- Practice Center 已重建全部 684 個題項。答案採分批獨立驗證；未完成驗算的題目明確標示 pending，不提供推測答案。
