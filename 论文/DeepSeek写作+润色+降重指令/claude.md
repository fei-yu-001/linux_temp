# 学术论文 AI 辅助写作指令手册

> 整合自 DeepSeek 喂饭指令系列文档，经去重、分类、优化后形成的一站式学术写作 Prompt 参考手册。
> 适用于 DeepSeek、Claude、Kimi、豆包等主流 AI 工具。

---

## 目录

1. [写作原则与注意事项](#一写作原则与注意事项)
2. [选题构思](#二选题构思)
3. [开题报告撰写](#三开题报告撰写)
4. [文献检索与综述](#四文献检索与综述)
5. [论文大纲构建](#五论文大纲构建)
6. [研究方法规划](#六研究方法规划)
7. [论文初稿撰写（按章节）](#七论文初稿撰写按章节)
8. [SCI 论文各模块撰写](#八sci-论文各模块撰写)
9. [数据分析与呈现](#九数据分析与呈现)
10. [案例分析与讨论](#十案例分析与讨论)
11. [论文润色指令](#十一论文润色指令)
12. [中英文翻译](#十二中英文翻译)
13. [查重降重指令](#十三查重降重指令)
14. [论文修改与完善](#十四论文修改与完善)
15. [参考文献整理](#十五参考文献整理)
16. [投稿审稿指令](#十六投稿审稿指令)
17. [辅助工具推荐](#十七辅助工具推荐)

---

## 一、写作原则与注意事项

1. **明确论文结构**：先确定论文结构和各部分主题，再引导 AI 生成文本，确保逻辑连贯。
2. **提供明确指令**：使用问句或指导性命令，让 AI 清晰了解你需要的内容和论据。
3. **限制生成长度**：通过限制每次生成长度避免冗长回答，集中获取真正需要的信息。
4. **逐步编辑完善**：AI 生成文本需人工编辑润色，确保逻辑一致、语法正确、符合学术规范。
5. **验证引用文献**：使用任何引述或信息时，验证并确保文献的准确性，正确引用参考文献。
6. **分步生成**：不要一次性要求生成整篇论文，按章节逐步生成效果更佳。
7. **投喂背景知识**：润色/翻译前先给 AI 投喂相关研究背景知识和目标期刊的写作风格，效果更精准。
8. **避免 AIGC 查重**：内容避免模板化和通用表达，使用专业术语，确保原创性和独特性。

---

## 二、选题构思

### 2.1 通用选题指令

> 我是【专业】学生，研究方向是【领域】，你将扮演我导师的角色。我对【技术/现象】感兴趣，但还没形成具体研究问题。请帮我推荐5个参考选题。

### 2.2 分学科选题

| 学科类型 | 指令要点 |
|---------|---------|
| **本科** | 以【专业领域】为范畴，结合社会热点，提供10个选题，每个附200字价值阐述 |
| **硕士** | 针对【行业细分方向】，挖掘5个创新性选题，体现学术前沿性和实践价值 |
| **博士** | 从【学科交叉领域】出发，生成8个选题，突出研究深度和理论贡献，附研究难点及解决思路 |
| **工科** | 基于【新兴技术趋势】，提供10个选题，强调技术应用创新和实际效益 |
| **人文社科** | 结合【文化现象或艺术潮流】，给出10个选题，阐述对文化传承或艺术发展的意义 |
| **公共管理** | 以【社会问题】为切入点，生成10个选题 |
| **工商管理** | 从【企业经营困境】角度，构思10个选题 |
| **教育学** | 围绕【教育改革热点】，提供10个选题 |
| **医学** | 基于【医疗行业新动态】，给出10个选题 |

---

## 三、开题报告撰写

### 3.1 选题背景

- **字数**：800字左右
- **内容**：领域背景 → 宏观背景 → 具体背景 → 研究问题 → 研究对象
- **要求**：层层递进，紧扣研究需求，避免泛泛而谈

### 3.2 研究目的

- **字数**：450±50字
- **内容**：
  - ① 研究目标：以解决实际问题为导向，目标务实、可测量
  - ② 研究范围：合理划定边界，涵盖变量或技术限制
  - ③ 创新点：避免"填补空白"等笼统表述，突出方法或应用上的优势

### 3.3 研究意义

- **字数**：500±50字
- **内容**：
  - ① 理论意义：丰富研究成果、发展理论框架、开辟新思路
  - ② 实践意义：提供科学依据、推动政策合理化、优化行业流程
  - ③ 社会影响：提升服务质量、减少资源浪费、推动可持续发展

### 3.4 国内外研究现状

#### 国内研究现状

- **字数**：2500±500字
- **结构**：无副标题，按自然段落分布
- **语言风格**：学术严谨、流畅精炼，模仿《Nature》风格
- **内容组成**：
  1. 研究历程与发展背景（约300字）
  2. 文献归纳、分析、叙述（至少2000字，每篇文献总结≥200字）
  3. 技术路径分析（约500字）
  4. 社会、国家与政策支持分析（约300字）

#### 国外研究现状

- **字数**：2000±100字
- **要求**：同国内研究现状的学术风格要求

### 3.5 主要内容和研究方法

- **主要内容**：350±50字（研究目标与核心问题、研究内容框架、研究重点与创新性）
- **研究方法**：350±50字（文献综述、数据收集与分析、模型建立、实验设计与验证、结果分析与解释）

### 3.6 前期基础和预期成果

- **前期基础**：350±50字（理论贡献与学术价值、实践应用与技术价值、成果展示与形式）
- **预期成果**：列出最终预期成果形式（学术论文、研究报告、数据集、算法模型等）

### 3.7 总体进度及安排

- **字数**：300-500字
- **内容**：阶段划分 + 时间节点 + 阶段任务与目标 + 进度表格或时间线
- **格式**：阶段-任务内容-起止时间-预期成果

---

## 四、文献检索与综述

### 4.1 文献检索指令

| 场景 | 指令 |
|------|------|
| 核心文献整理 | 针对【论文选题】，检索近5年相关文献，整理10篇核心文献的作者、标题、期刊、年份、摘要和关键词 |
| 外文文献综述 | 围绕【研究主题】，检索筛选10篇高质量外文文献，翻译并提炼核心观点，形成1500字综述 |
| 分类文献综述 | 以【关键词组】为检索依据，收集20篇文献，按研究内容分类，撰写2000字综述 |
| 行业报告检索 | 针对【选题领域】，检索最新行业报告和政策文件，整理5份重要资料 |
| 理论应用检索 | 围绕【经典理论】，检索其在【研究领域】的应用文献，撰写1800字综述 |
| 方法案例检索 | 以【研究方法】为线索，整理10篇运用该方法的成功案例 |
| 跨学科综述 | 针对【跨学科选题】，从不同学科各收集5篇核心文献，撰写2000字跨学科综述 |
| 会议论文检索 | 围绕【研究热点】，检索近3年会议论文，整理10篇创新性论文 |
| 学者研究综述 | 以【知名学者研究方向】为导向，收集10篇代表作，撰写1500字学者研究综述 |
| 概念综述 | 针对【新兴概念】，收集10篇最早提出该概念的文献，撰写1800字概念综述 |

### 4.2 文献综述撰写指令

> 请帮我写一份关于【研究主题】的文献综述。我的选题方向是XX，已找到以下文献：
> （文献1的标题、作者、出版年份、摘要和关键词）
> （文献2的标题、作者、出版年份、摘要和关键词）
> ...
> 请按以下结构组织：引言（背景、意义、目的）→ 主体（按主题/方法/观点分类）→ 结论（主要发现、贡献和不足）

### 4.3 精准文献综述（进阶）

> 总结近5年关于"XXX主题"的国内外研究，按"支持派/反对派/中立派"分类，并指出争议焦点。要求每类研究至少引用3篇权威文献，并附上每篇文献的核心观点。

> 当前关于XXX主题的研究空白是什么？请结合最新文献提出3个可能的研究方向，并附上相关文献支持。

---

## 五、论文大纲构建

| 论文类型 | 大纲要求 |
|---------|---------|
| **本科** | 引言+正文+结论，正文至少3章，每章有明确标题和内容描述 |
| **硕士** | 体现深度和逻辑性，正文4-5章，每章有详细子标题和内容要点 |
| **博士** | 突出创新性和理论贡献，正文5-6章，深入阐述研究内容 |
| **文科** | 注重理论分析和逻辑论证，按"问题提出→分析→解决"组织 |
| **理科** | 强调实验研究和数据分析，按"实验设计→过程→结果分析→结论"展开 |
| **工科** | 突出技术应用和创新，包括需求分析、方案设计、技术实现、测试验证 |
| **商科** | 注重案例分析和实践应用，包括案例介绍、问题分析、解决方案、效果评估 |
| **教育类** | 结合教育实践和理论研究，包括现状分析、问题探讨、策略建议 |
| **医学类** | 围绕临床研究，包括病例分析、病因探讨、治疗方法、预后评估 |

### 大纲生成指令

> 请生成一篇关于"XXX主题"的论文大纲，包含：【研究背景与意义、文献综述、研究方法、数据分析与结果、讨论与建议】。要求每个部分详细列出子标题，并附上核心内容概述。

> 追加：请补充每个章节需要解决的核心问题。

---

## 六、研究方法规划

| 方法 | 指令要点 |
|------|---------|
| **问卷调查法** | 问卷设计、样本选取、数据收集和分析方法、可能遇到的问题及解决措施 |
| **访谈法** | 访谈提纲设计、访谈对象选择、访谈记录和整理分析 |
| **案例分析法** | 案例选择、资料收集、案例分析和结论总结 |
| **实验研究法** | 实验设计、变量控制、数据测量和结果分析 |
| **文献研究法** | 文献检索、筛选、阅读和整理，成果应用 |
| **扎根理论法** | 资料收集、编码分析、理论构建和验证 |
| **比较研究法** | 比较对象确定、比较指标选择、比较分析和结论 |
| **内容分析法** | 分析单位确定、分析框架制定、内容编码和数据分析 |
| **行动研究法** | 问题提出、计划制定、行动实施、观察记录和反思调整 |
| **德尔菲法** | 专家选择、问卷设计、多轮调查和数据处理 |

### 研究理论推荐指令

> 我是【专业】学生，研究方向是【领域】，你将扮演我导师角色。我目前确定的选题是【XX】，请从【方向】出发，推荐5个适合的研究理论，给出理论名称、作者、出处和主要观点。

---

## 七、论文初稿撰写（按章节）

### 7.1 摘要

> 本文旨在探讨XX领域中的关键议题，通过系统梳理国内外研究现状，明确了当前研究的不足与空白。在此基础上，本文采用XX研究方法，对XX问题进行了深入分析，揭示了XX现象的本质及其背后的机制。研究发现，XX因素在XX过程中发挥了重要作用，并提出了一系列针对性的建议。本研究不仅丰富了XX领域的理论体系，也为实践应用提供了有价值的参考。

- 字数：一般不超过250字

### 7.2 绪论

| 小节 | 内容要点 |
|------|---------|
| 研究背景 | 领域重要性、当前存在的问题或研究空白 |
| 研究意义 | 理论意义（填补空白、构建理论体系）+ 实践意义（指导应用、推动发展）+ 社会价值 |
| 研究内容 | 全面剖析现象 → 探讨影响因素 → 提出解决方案 → 可行性论证 → 效果预测评估 |
| 研究方法 | 文献综述法 + 实证研究方法 + 定量定性分析 + 比较分析法 |

### 7.3 文献综述

- **国外研究现状**：聚焦现象解释、影响因素分析、解决方案，指出争议和差异
- **国内研究现状**：梳理研究成果，指出深度、广度及创新性方面的不足

### 7.4 正文（本论）

按"存在问题 → 分析问题 → 论证观点 → 对策办法"四步展开：

1. **存在问题**：数据局限性、理论框架不完善、忽略潜在影响因素
2. **分析问题**：多维度分析、量化分析影响因素、探讨相互作用机制
3. **论证观点**：多维度对比分析、理论模型与实证数据验证、综合讨论
4. **对策办法**：源头管理、资源优化配置、宣传教育

### 7.5 结论

总结主要发现与学术贡献 → 概括对实践/产业/社会的潜在影响 → 分析局限性 → 提出未来研究方向

### 7.6 致谢

> 我想请你帮我写一份论文致谢，论文题目是【XX】，导师是【XX】，合作者是【XX】，感谢对象及贡献如下...请使用礼貌和感恩的语气，约【字数】字。

---

## 八、SCI 论文各模块撰写

### 8.1 标题 (Title)

> 请帮我生成3个备选标题，要求：1.包含关键词【XX】；2.突出创新点【XX】；3.符合【目标期刊】的标题风格。

### 8.2 摘要 (Abstract)

> 请帮我写一个250词的摘要。要求：背景（现有局限）→ 方法（合成与功能化、实验设计）→ 结果（关键数据）→ 结论（临床转化潜力）。明确各部分字数分配（如背景20%、方法30%、结果40%、结论10%）。

### 8.3 关键词 (Keywords)

> 请帮我列出5-6个关键词，避免与标题完全重复，覆盖研究领域、方法、应用场景。

### 8.4 引言 (Introduction)

提供逻辑链条："领域背景 → 未解决问题 → 本研究策略"

> 请帮我写引言，结构如下：
> 1. 第一段：XX领域现状（引用3篇高被引综述）
> 2. 第二段：XX技术在克服XX中的作用（引用2篇关键论文）
> 3. 第三段：指出XX的潜力及当前挑战
> 4. 最后一段：本研究的目标和创新点

### 8.5 材料与方法 (Materials and Methods)

分模块描述：材料（纯度、供应商、细胞系来源）→ 合成步骤（详细参数）→ 表征技术 → 动物实验（伦理审批号、模型建立、给药方案）→ 数据分析方法

### 8.6 结果 (Results)

按逻辑顺序排列数据（"表征 → 体外 → 体内"），标注图表引用。

### 8.7 讨论 (Discussion)

> 请帮我写讨论部分，需包含：1.与文献对比的优势；2.效果差异的可能原因；3.局限性；4.未来方向。

### 8.8 结论 (Conclusion)

避免重复结果，强调普适性意义。

### 8.9 其他模块

- **图表设计**：提供需要插入的图表和数据
- **参考文献**：整理并格式化，确保符合SCI期刊格式
- **Cover Letter**：强调研究创新点和期刊匹配度
- **补充材料**：详细实验步骤、额外数据图表
- **回复审稿意见**：逐条回复，说明修改内容

---

## 九、数据分析与呈现

| 工具 | 分析类型 | 指令要点 |
|------|---------|---------|
| SPSS | 描述性统计 | 生成分析结果并撰写报告，解释各项统计指标 |
| Excel | 数据清洗/透视表 | 展示操作步骤和处理前后对比 |
| Python | 相关性分析 | 展示代码和分析结果，说明变量相关性 |
| Stata | 回归分析 | 解释模型构建过程、结果解读和适用性 |
| SPSS | 因子分析 | 展示分析过程和结果，解释因子含义和命名 |
| AMOS | 结构方程模型 | 展示模型构建、拟合度检验和结果分析 |
| R | 聚类分析 | 展示聚类结果和可视化图表 |
| SPSS | 方差分析 | 说明不同组之间的差异及其显著性 |
| Eviews | 时间序列分析 | 展示分析过程和预测结果 |

---

## 十、案例分析与讨论

按领域选择典型案例进行深入分析：

- **企业案例**：背景、发展历程、面临问题，运用理论分析（2000字）
- **社会现象案例**：具体情况和影响，原因和解决途径（1800字）
- **教育实践案例**：实施过程和效果，成功经验和不足（2000字）
- **医疗案例**：病例情况、诊断过程和治疗方法（1800字）
- **政策实施案例**：政策内容、实施过程和效果（1800字）
- **科技创新案例**：创新点、技术应用和市场前景（2000字）

---

## 十一、论文润色指令

### 11.1 学术角色预设

> As a leader in the academic field, I possess extensive academic experience and professional knowledge across various domains. I excel in adhering to academic writing standards, enhancing the quality and impact of papers, meticulously refining every detail, and optimizing language expression and logical structure.

### 11.2 论文评审专家模式

> 你现在扮演一个【研究领域】领域的专家，从专业角度，指出需要修改的地方，给出修改意见及推荐修改内容。注意不要全文修改，逐一指出。

### 11.3 英文润色

| 编号 | 指令 | 适用场景 |
|------|------|---------|
| 1 | Refinish writing to conform to academic style, improve spelling, grammar, clarity, conciseness and overall readability. List all modifications in Markdown table and explain reasons. | 通用英文润色 |
| 2 | Polish the writing to meet academic style. List all modification and explain the reasons in markdown table. | 带修改说明的润色 |
| 3 | Enhance the spelling, grammar, clarity, conciseness, and overall readability. Breakdown long sentences, reduce repetition. Provide only the corrected version without explanations. | 精简版润色 |
| 5 | SCI论文润色：Correct grammatical errors, improve sentence structure, make text more formal. Put all modified sentences in Markdown table (original sentence → revised part → explanation). Finally, rewrite the full corrected paragraph. | SCI投稿级润色 |
| 6 | 润色段落结构和句子逻辑：Analyze the logic and coherence among sentences, identify areas where flow could be improved, provide specific suggestions. | 逻辑连贯性优化 |

### 11.4 中文润色

> 作为一名中文学术论文写作改进助理，你的任务是改进所提供文本的拼写、语法、清晰、简洁和整体可读性，同时分解长句，减少重复，并提供改进建议。请只提供文本的更正版本，避免包括解释。

### 11.5 语法检查

> Can you help me ensure that the grammar and the spelling is correct? Do not try to polish the text. If no mistake is found, tell me this paragraph is good. If you find grammar or spelling mistakes, please list mistakes in a two-column markdown table.

### 11.6 个性化润色维度

- **More precise**：选择更精确的词汇（如用"generate"代替"produce"）
- **More concise**：去除冗余表达
- **More objective**：剔除含糊和主观性表述
- **More specific**：提供具体细节支持论点
- **More coherent**：确保句子组织性良好、逻辑流畅
- **More consistent**：确保用词和语调与整篇论文保持一致
- **More academic**：运用正确的学术用语
- **More formal grammar**：使用正确的语法或句法
- **More nuanced**：使用精准词汇描述复杂概念

### 11.7 重新回答

> Still the above question, I think your answer is not good enough. Please answer again, this time focusing on removing redundancy from this passage.

### 11.8 润色定位

> 注意，除了给出润色修改之后的内容，还请明确修订版本中具体修改了哪些段落的哪几句话。（建议让AI给出润色前后的对比版本，使用表格输出）

### 11.9 逻辑论证辅助

> Please help me analyze and optimize the logical structure of this argument to make it more convincing.

---

## 十二、中英文翻译

### 12.1 论文翻译（中→英）

> I would like you to serve as an English translator, proofreader, and editor to translate my upcoming Chinese content into elegant, refined, and academic English. Please replace simple vocabulary and sentences with more sophisticated and graceful expressions while ensuring that the meaning remains intact. Overall, the language style should be similar to the【目标期刊】academic journal.

### 12.2 中译英（双版本对照）

> I am a researcher studying【研究方向】, now trying to revise my manuscript which will be submitted to【投稿期刊】. I want you to act as a scientific English-Chinese translator. Give the output in a markdown table: first column is the original language, second is the first version of translation, third is the second version, and give each row only one sentence.

### 12.3 中英互译

> I want you to act as a scientific English-Chinese translator. I will provide some paragraphs in one language and your task is to accurately and academically translate the paragraphs only into the other language. Do not repeat the original provided paragraphs after translation.

---

## 十三、查重降重指令

| 方法 | 英文指令 | 中文说明 |
|------|---------|---------|
| **内容降重** | If there are 13 consecutive identical words, they will be considered as duplication. Use methods such as adjusting word order, replacing synonyms, adding or deleting words. | 连续13字相同算重复，调整主谓宾语序、替换同义词、增减字数 |
| **改写降重** | Rephrase by adjusting word order, modifying length, and substituting synonyms to avoid any sequence of 8 consecutive words that match the original. | 避免连续8字相同，调整语序、增减字数、替换同义词 |
| **同义词替换** | Adjust logical structure, employ active/passive voice interchange, synonym replacement, paraphrasing with near-synonyms. Break down complex sentences and reduce repetition. | 交替使用主被动语态、替换同义词、近义词意译、拆分复杂句 |
| **避免连续相同** | Reduce repetition by adjusting word order, modifying length, substituting synonyms to avoid any sequence of 8 consecutive words matching the original. | 避免连续8字相同 |
| **缩写扩写降重** | Rewrite by adjusting word order, substituting synonyms to avoid 3 consecutive words matching. Then expand upon the content. Finally condense it to fit academic paper style. | 先改写避免连续3字相同，再扩写，最后缩写 |
| **句式变换降重** | Change grammatical constructions and incorporate alternative expressions to avoid any sequence of 5 consecutive words identical to the original. | 改变句法结构，避免连续5字相同 |
| **逻辑重组** | Reorganize the logic by restructuring sentences and paragraphs, ensuring flow of ideas is coherent and distinct from the original. | 重构句子和段落逻辑 |
| **综合改写** | Revise by integrating new ideas and perspectives, rephrasing to ensure content is unique and adheres to academic standards. | 整合新想法和视角，确保独特性 |
| **概念解释降重** | Explain concepts in your own words after understanding their meaning, to reduce reliance on original text. | 用自己的话解释概念 |

---

## 十四、论文修改与完善

| 维度 | 检查要点 |
|------|---------|
| **格式审查** | 按学校规定格式要求，指出格式错误并提出修改建议 |
| **逻辑结构** | 分析各章节连贯性和逻辑性，提出优化建议 |
| **内容完整性** | 检查研究内容是否缺失或不深入，提出补充建议 |
| **语言表达** | 修改语法错误、用词不当和语句不通顺 |
| **参考文献** | 检查引用格式是否正确，文献数量是否符合要求 |
| **图表规范** | 检查标题、编号、数据标注是否符合要求 |
| **论证过程** | 检查论据是否充分、论证是否有力 |
| **创新性** | 分析研究成果的学术价值和实践意义 |
| **摘要关键词** | 检查摘要是否准确概括核心内容，关键词是否恰当 |
| **致谢** | 检查表达是否真诚、恰当 |

---

## 十五、参考文献整理

| 场景 | 指令 |
|------|------|
| 格式整理 | 按照【学校格式】，整理【引用的参考文献】，生成参考文献列表 |
| 中文核心推荐 | 为【选题】推荐10篇中文核心期刊文献，注明作者、标题、期刊、年份、卷号、页码 |
| 外文权威推荐 | 围绕【领域】，推荐8篇外文权威期刊文献，附中文翻译 |
| 引用恰当性检查 | 以【初稿】为基础，检查引用是否恰当、与内容是否紧密相关 |
| 行业报告收集 | 针对【选题】，收集5篇最新行业报告，整理标题、机构、时间和摘要 |
| 学术著作推荐 | 为【研究】推荐3本学术著作，列出作者、书名、出版社、年份和章节 |
| 学位论文整理 | 查找5篇学位论文，注明作者、授予单位、学位类型、题目和答辩年份 |
| 时效性检查 | 以【初稿】为依据，检查参考文献时效性，补充最新成果 |
| 会议论文收集 | 收集2篇会议论文，整理作者、标题、会议名称、时间和地点 |
| 注释整理 | 按规范格式对文中引用进行注释，确保准确、清晰 |

### 参考文献格式检查指令

> I'd like you to serve as a reference editor. I will supply five reference templates as guidelines. Then I will provide additional references for which you'll need to examine formatting aspects. Provide a markdown table with three columns: original text | fixed text | explanation.

---

## 十六、投稿审稿指令

### 16.1 撰写 Cover Letter

> I want you to act as an academic journal editor. I will provide the title and abstract of my manuscript. You need to write a formal cover letter for submitting to【目标期刊】. You should state that the manuscript has not been considered for publication in any other journal. Briefly introduce the merit and provide a short summary to point out the importance of the results.

### 16.2 解释审稿人反馈

> Act as an academic research expert. Carefully analyze and interpret the feedback provided by the reviewer. Identify key concerns, constructive suggestions, and areas of improvement. Create a detailed response plan.

### 16.3 审稿意见解读与分析

> Please interpret and analyze the reviewer's comments: which need to be focused on and which are of secondary importance. Also give revisions based on my article and analyze how to revise, and give why.

### 16.4 回复审稿意见

> 请帮我撰写回复审稿意见的稿件，针对每位审稿人的意见逐条回复，并说明如何修改论文以回应这些意见。

---

## 十七、辅助工具推荐

### 写作效率

| 工具 | 用途 |
|------|------|
| Grammarly | 语法和拼写检查 |
| Hemingway Editor | 简化复杂句子，提升可读性 |
| Paperpal | AI辅助润色，匹配学术表达 |
| Zotero | 文献管理+一键插入引用 |
| EndNote | 支持99%期刊格式，批量调整引用 |
| Mendeley | 免费云同步，团队协作管理文献 |

### 数据分析

| 工具 | 用途 |
|------|------|
| GraphPad Prism | 统计分析与科研图表 |
| Python/Matplotlib | 灵活绘制高自由度科研图表 |
| ImageJ | 量化显微镜图像 |
| Tableau | 交互式数据展示 |
| SPSS | 描述性统计、因子分析、方差分析 |
| OriginLab | 科研级数据绘图 |

### 图表设计

| 工具 | 用途 |
|------|------|
| BioRender | 专业绘制生物学示意图 |
| Adobe Illustrator | 矢量图编辑，满足期刊高清排版 |
| LabArchives | 电子实验记录本 |

### 文献检索

| 工具 | 用途 |
|------|------|
| Connected Papers | 可视化领域文献网络 |
| Research Rabbit | 智能分析领域文献趋势 |
| Scite | 查看文献引用上下文 |
| Google Scholar | 学习高被引论文标题风格 |

### 数据管理

| 工具 | 用途 |
|------|------|
| Figshare | 公开数据并生成DOI |
| GitHub | 管理代码+版本控制 |
| Google Drive | 团队协作存储 |

### 投稿相关

| 工具 | 用途 |
|------|------|
| AJE Cover Letter | 投稿信模板库 |
| Cite This For Me | 快速生成单篇文献标准格式 |
| LaTeX | 复杂公式与排版 |

### 一句话总结

- **效率提升**：Grammarly修语言，Zotero管文献，BioRender画图
- **数据严谨**：GraphPad做统计，ImageJ量化图像，Figshare存数据
- **投稿省心**：EndNote调格式，AJE写投稿信，Excel跟审稿

---

## 附录：通用 Prompt 模板速查

### 角色设定

```
我是【专业】学生，研究方向是【领域】，你将扮演我导师的角色。
```

### 选题

```
请从【方向】出发，推荐【数量】个选题，附选题价值阐述/研究难点/创新点。
```

### 大纲

```
请生成关于"【主题】"的论文大纲，包含【各部分】，每部分列出子标题和核心内容概述。
```

### 初稿（按章节扩写）

```
请根据大纲扩写"【章节名】"部分，要求结合最新研究趋势/详细说明方法/结合假设和数据。
```

### 润色

```
请润色以下段落，符合学术风格，提高语法、清晰度和可读性。在Markdown表格中列出修改及原因。
```

### 降重

```
请改写这段话，通过调整语序、替换同义词等方式，避免与原文出现连续【N】个字相同，使内容更有逻辑、符合论文规范。
```

### 翻译

```
请将以下中文内容翻译成优雅、精炼、学术化的英文，语言风格类似【目标期刊】。
```
