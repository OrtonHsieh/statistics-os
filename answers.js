/* Independently checked answers. Missing IDs remain explicitly unverified. */
const VERIFIED_ANSWERS={};
const addMC=(chapter,number,letter,note='Definition or calculation independently rechecked.')=>{
  VERIFIED_ANSWERS[`ch${chapter}-mc-${String(number).padStart(3,'0')}`]={status:'verified',answer:letter.toUpperCase(),confidence:'high',explanation:note};
};

// Chapter 12: verified against the definitions/calculations and the publicly
// available matching answer-key preview for the same test-bank edition.
['A','D','B','D','C','A','C','B','D','D','D','D','C','A','A','B','A','C','D','A','D','B','C','A','A','D','D','C','C','A','B','B','C','C','D','D','D','A','A','C','C','B','A','A','D','B','A'].forEach((a,i)=>addMC(12,i+1,a));

// Chapter 13, first principles / ANOVA identities; cross-checked with the
// matching public answer-key preview.
['B','B','C','D','A','A','B'].forEach((a,i)=>addMC(13,i+1,a));

// Chapter 17: all 37 MC items independently definition-checked or recomputed.
['B','B','D','C','B','D','A','C','A','B','C','C','C','B','C','B','A','B','D','B','B','B','A','D','C','D','C','C','B','B','A','C','D','A','C','C','B'].forEach((a,i)=>addMC(17,i+1,a));

// Chapter 18 foundational nonparametric concepts and Spearman calculation.
['B','D','A','D','B','D','C','D','B','B','A','B','A','B','D','A','C','A','D','B','C','A','D','C','D','D','D','A','D','D','A','D','A','A','A','A','B','D','B','A','B','C','B','A','B','C','D','B','C','B','B','A','B'].forEach((a,i)=>addMC(18,i+1,a));

Object.assign(VERIFIED_ANSWERS,{
  'ch12-problem-001':{status:'verified',confidence:'high',answer:`a. χ² = 18.4232.\nb. df=2, p≈0.00010; reject H₀.\nc. χ².05,2=5.991; 18.4232>5.991, reject H₀.`,explanation:`H₀: the candidate proportions remain 34%, 43%, and 23%. Expected counts are 136, 172, and 92. χ²=Σ(O−E)²/E=18.4232. The campaign-period sample provides strong evidence that the preference proportions changed.`},
  'ch12-problem-003':{status:'verified',confidence:'high',answer:`H₀: illness is independent of smoking. H₁: they are not independent.\nExpected table: (32,48), (60,90), (28,42).\nχ²=10.5159, df=2, p≈0.0052. Reject H₀ at α=.05.`,explanation:`Each expected count is row total × column total / 300. Since 10.5159>χ².05,2=5.991, illness type and smoking status are associated in this sample. Association alone does not establish causation.`},
  'ch13-problem-020':{status:'verified',confidence:'high',answer:`H₀: μA=μB=μC=μD; H₁: not all means are equal.\nMeans: 145, 135, 190, 150; grand mean=155.\nSSTR=8,750; SSE=7,600; SST=16,350.\nANOVA: treatment df=3, MSTR=2,916.667; error df=16, MSE=475; F=6.1404; p≈.0056. Reject H₀.\nFisher LSD=29.22. C differs from A, B, and D; the other pairs do not differ significantly.`,explanation:`The overall F test must be significant before the protected LSD comparisons. Program C has the highest mean output and is the only program separated from each of the other three by more than the LSD.`},
  'ch14-problem-001':{status:'verified',confidence:'high',answer:`a. ŷ=1.04155+0.00990716x.\nb. R²=0.56291: about 56.29% of sample price variation is explained by pages.\nc. r=0.75027; t=2.5376 (df=5), equivalent F=6.4392. At α=.10, reject H₀:β₁=0.`,explanation:`The slope is positive: one additional page is associated with about $0.00991 higher predicted price within the observed range. This is association, not a causal conclusion.`},
  'ch14-problem-003':{status:'verified',confidence:'high',answer:`a. ŷ=29.78571−0.728571x; each $1 increase in price is associated with about 0.729 fewer units sold.\nb. R²=0.85559.\nc. r=−0.92498; t=−5.4428 (df=5), F=29.6241. At α=.01, reject H₀:β₁=0.`,explanation:`The fitted relationship is strong and negative. The sign of r follows the sign of the slope, and r² equals R² in simple regression.`},
  'ch15-problem-006':{status:'verified',confidence:'high',answer:`a. ŷ=7.0174+8.6233X₁+0.0858X₂.\nb. At X₁=3.5 and X₂=45: ŷ=41.05995 million dollars = $41,059,950.\nc. F=17.7297 with df=(2,7); the overall model is significant at α=.05.\nd. t for β₁=3.5978 with df=7; advertising is significant.\ne. R²=321.11/(321.11+63.39)=0.83514.\nf. Adjusted R²=0.78803.`,explanation:`The overall F asks whether all slopes are zero jointly. The individual advertising t test asks whether β₁ is zero while holding the number of salespeople constant.`},
  'ch16-problem-010':{status:'verified',confidence:'high',answer:`Partial F=[(1425−1300)/1]/[1300/(28−3−1)]=2.3077. With df=(1,24), p≈.142; do not reject H₀ at α=.05. Do not add X₃ solely on this evidence.`,explanation:`The full model contains three predictors, so its error df is 28−3−1=24. The decrease in SSE is not large enough relative to the full-model error variance.`},
  'ch17-problem-002':{status:'verified',confidence:'high',answer:`Weights from oldest to newest are 2,3,5.\nApril=50.0; May=56.1; June=66.9; July=78.0.`,explanation:`For July: [2(60)+3(75)+5(87)]/10=78. The largest weight must be assigned to the most recent month.`},
  'ch17-problem-005':{status:'verified',confidence:'high',answer:`With α=.2 and FJan=18:\nFFeb=18.00; FMar=19.00; FApr=19.20; FMay=18.56.`,explanation:`Use F(t+1)=αA(t)+(1−α)F(t). The April actual value is used to create the May forecast, not the April forecast.`},
  'ch18-problem-001':{status:'verified',confidence:'high',answer:`Exclude 10 no-preference responses: n=390.\nH₀:p=.5; H₁:p≠.5.\nμ=np=195; σ=√[np(1−p)]=√97.5=9.8742.\nz≈(250−195)/9.8742=5.570 (5.52 with continuity correction). Reject H₀.`,explanation:`The evidence shows a difference in preference, with domestic wine preferred more often. Ties are excluded from the sign-test sample size.`},
  'ch18-problem-008':{status:'verified',confidence:'high',answer:`Rank differences are 1, −2, −1, 0, 2; Σd²=10.\nrₛ=1−6(10)/[5(5²−1)]=0.50. The correlation is not significant at α=.05 for n=5.`,explanation:`The two employers have a moderate positive rank association, but five candidates provide insufficient evidence for statistical significance.`}
});
