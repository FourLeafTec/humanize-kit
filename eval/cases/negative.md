# 正常人类文本（negative cases）

误改率基线：正常写作的文本，模型不应擅自改写。若被改动且无编辑收益，记一次误改（目标 < 10%）。

## N1 工作同步（事实陈述，无套话）

> 本次调整了重试策略，重复请求从 24 次降到 7 次。下周我先把登录模块的测试补完，再开始接支付回调。之前提的权限拆分方案需要产品确认后才能动。

## N2 个人随笔（有个性的表达，非模板）

> 周末把阳台的三角梅修了修，剪下来的枝条插在窗台水瓶里，两天就发了新芽。其实没指望它能活，就是顺手。我妈说我养花全凭运气，我倒觉得运气也是本事的一种。

## N3 英文邮件（简洁直白）

> The build failed on the staging server at 14:32. The error is a missing environment variable in the deploy script. I've fixed it locally and am re-running the pipeline now. Will update you once it's green.
