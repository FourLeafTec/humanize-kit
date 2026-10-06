# 待改善文本（positive cases）

改写任务的输入样例。构造样本，用于评测改写质量；每个样本标注了主要痕迹模式编号（对照 `references/patterns.md`）。

## P1 产品公告（A1 假对比 + E22 客服腔 + C13 意义拔高 + F31 套话收尾）

> 本次发布的 v3.2 更新不仅是功能的升级，更是我们团队对创新的一次深刻践行。它不仅带来了更快的加载速度（平均提升 24%），还新增了离线模式。而且，这次更新彰显了我们对用户体验的坚定承诺，标志着产品发展的关键转折点。最后，我想说，希望这次更新能给大家带来惊喜，让我们共同期待更美好的未来！

主要模式：A1、C13、C18（彰显/标志着）、E22、F31。

## P2 技术总结（F27 进行+动词 + F28 被字句堆叠 + F29 四字词排比 + F26 长定语）

> 针对线上服务所面临的高并发场景下的请求延迟问题，我们进行了深入调研，并对现有架构进行了全面优化。通过多轮测试，该问题已被有效缓解，系统的吞吐量已被显著提升，从每秒 800 请求提升至每秒 2400 请求。整个项目团队凝心聚力、攻坚克难、精准发力、扎实推进，最终取得了阶段性成果。

主要模式：F26、F27、F28、F29、C13、B6。

## P3 公众号开头（F30 万能背景 + A4 起跑式铺垫 + A3 伪深度）

> 在当今这个信息爆炸的时代，每个人都被海量的数据所包围。让我们先来思考一个问题：我们每天真正能够记住的内容有多少？说实话，这个问题没有标准答案。但归根结底，真正重要的不是我们看到了什么，而是我们如何选择。今天，我们就来聊聊内容筛选这件事。

主要模式：F30、A4、A3、B7（重复"我们"句首）。

## P4 英文公告（A1 + A2 + C13 + B8）

> It's not just an update, it's a revolution in how we think about productivity. We've completely redesigned our interface, and the results are nothing short of remarkable. Load times have dropped by 40%, and our users report saving an average of 2 hours per week. This marks a pivotal moment in our company's journey. Let that sink in.

主要模式：A1、A2、C13、B8、B6。
