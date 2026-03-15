export const messages = {
  en: {
    common: {
      language: 'Language',
      english: 'English',
      chinese: 'Chinese',
      refresh: 'Refresh',
      loading: 'Loading...',
      none: 'None'
    },
    home: {
      github: 'Visit our GitHub',
      tag: 'A simple, universal swarm-intelligence engine',
      version: '/ v0.1-preview',
      titleLine1: 'Upload any report',
      titleLine2: 'simulate the future now',
      description1:
        'Even a single text snippet can seed a parallel world in MiroFish, with up to millions of agents generated automatically from real-world context. From a god-view, you can inject variables and search for local optima inside dynamic collective behavior.',
      slogan: 'Rehearse the future through agents, and make decisions after a hundred simulations',
      systemStatus: 'System Status',
      readyTitle: 'Ready',
      readyDescription:
        'The prediction engine is standing by. Upload multiple unstructured documents to initialize a simulation sequence.',
      metrics: {
        lowCostTitle: 'Low Cost',
        lowCostLabel: 'Typical simulation averages about $5/run',
        highScaleTitle: 'High Scale',
        highScaleLabel: 'Supports up to millions of agents'
      },
      workflowTitle: 'Workflow Sequence',
      workflow: [
        {
          title: 'Graph Build',
          desc: 'Extract real-world seeds, inject individual and collective memory, and construct GraphRAG.'
        },
        {
          title: 'Environment Setup',
          desc: 'Extract entities and relationships, generate personas, and inject simulation parameters.'
        },
        {
          title: 'Run Simulation',
          desc: 'Simulate across dual platforms, parse the prediction request, and update temporal memory.'
        },
        {
          title: 'Generate Report',
          desc: 'Let ReportAgent use a rich toolset to interrogate the post-simulation environment.'
        },
        {
          title: 'Deep Interaction',
          desc: 'Talk to any simulated actor or continue the analysis with ReportAgent.'
        }
      ],
      realitySeed: '01 / Reality Seed',
      uploadFormats: 'Supported: PDF, MD, TXT',
      dragTitle: 'Drag files here',
      dragHint: 'or click to browse the filesystem',
      inputParams: 'Input Parameters',
      promptLabel: '>_ 02 / Simulation Prompt',
      promptPlaceholder:
        '// Describe the simulation or prediction request in natural language (e.g. what public reaction follows if a university reverses a disciplinary announcement?)',
      engineBadge: 'Engine: MiroFish-V1.0',
      startEngine: 'Start Engine',
      initializing: 'Initializing...',
      researchMode: 'Enter Research Mode'
    },
    history: {
      title: 'Simulation Archive',
      graphBuild: 'Graph Build',
      envSetup: 'Environment Setup',
      report: 'Analysis Report',
      moreFiles: '+{count} more files',
      noFiles: 'No files',
      loading: 'Loading...',
      requirement: 'Simulation Requirement',
      relatedFiles: 'Related Files',
      noRelatedFiles: 'No related files',
      replay: 'Replay',
      step1: 'Graph Build',
      step2: 'Environment Setup',
      step4: 'Analysis Report',
      replayHint:
        'Step 3 "Run Simulation" and Step 5 "Deep Interaction" must be launched live and are not available for replay.',
      untitled: 'Untitled Simulation',
      notStarted: 'Not started',
      rounds: '{current}/{total} rounds',
      unknownFile: 'Unknown file',
      loadError: 'Failed to load history projects:'
    },
    research: {
      mode: 'Research Mode',
      refreshProjects: 'Refresh Projects',
      refreshingProjects: 'Refreshing...'
    }
  },
  zh: {
    common: {
      language: '语言',
      english: '英文',
      chinese: '中文',
      refresh: '刷新',
      loading: '加载中...',
      none: '无'
    },
    home: {
      github: '访问我们的Github主页',
      tag: '简洁通用的群体智能引擎',
      version: '/ v0.1-预览版',
      titleLine1: '上传任意报告',
      titleLine2: '即刻推演未来',
      description1:
        '即使只有一段文字，MiroFish 也能基于其中的现实种子，全自动生成与之对应的至多百万级Agent构成的平行世界。通过上帝视角注入变量，在复杂的群体交互中寻找动态环境下的“局部最优解”。',
      slogan: '让未来在 Agent 群中预演，让决策在百战后胜出',
      systemStatus: '系统状态',
      readyTitle: '准备就绪',
      readyDescription: '预测引擎待命中，可上传多份非结构化数据以初始化模拟序列',
      metrics: {
        lowCostTitle: '低成本',
        lowCostLabel: '常规模拟平均5$/次',
        highScaleTitle: '高可用',
        highScaleLabel: '最多百万级Agent模拟'
      },
      workflowTitle: '工作流序列',
      workflow: [
        {
          title: '图谱构建',
          desc: '现实种子提取 & 个体与群体记忆注入 & GraphRAG构建'
        },
        {
          title: '环境搭建',
          desc: '实体关系抽取 & 人设生成 & 环境配置Agent注入仿真参数'
        },
        {
          title: '开始模拟',
          desc: '双平台并行模拟 & 自动解析预测需求 & 动态更新时序记忆'
        },
        {
          title: '报告生成',
          desc: 'ReportAgent拥有丰富的工具集与模拟后环境进行深度交互'
        },
        {
          title: '深度互动',
          desc: '与模拟世界中的任意一位进行对话 & 与ReportAgent进行对话'
        }
      ],
      realitySeed: '01 / 现实种子',
      uploadFormats: '支持格式: PDF, MD, TXT',
      dragTitle: '拖拽文件上传',
      dragHint: '或点击浏览文件系统',
      inputParams: '输入参数',
      promptLabel: '>_ 02 / 模拟提示词',
      promptPlaceholder:
        '// 用自然语言输入模拟或预测需求（例.武大若发布撤销肖某处分的公告，会引发什么舆情走向）',
      engineBadge: '引擎: MiroFish-V1.0',
      startEngine: '启动引擎',
      initializing: '初始化中...',
      researchMode: '进入研究模式'
    },
    history: {
      title: '推演记录',
      graphBuild: '图谱构建',
      envSetup: '环境搭建',
      report: '分析报告',
      moreFiles: '+{count} 个文件',
      noFiles: '暂无文件',
      loading: '加载中...',
      requirement: '模拟需求',
      relatedFiles: '关联文件',
      noRelatedFiles: '暂无关联文件',
      replay: '推演回放',
      step1: '图谱构建',
      step2: '环境搭建',
      step4: '分析报告',
      replayHint: 'Step3「开始模拟」与 Step5「深度互动」需在运行中启动，不支持历史回放',
      untitled: '未命名模拟',
      notStarted: '未开始',
      rounds: '{current}/{total} 轮',
      unknownFile: '未知文件',
      loadError: '加载历史项目失败:'
    },
    research: {
      mode: '研究模式',
      refreshProjects: '刷新项目',
      refreshingProjects: '刷新中...'
    }
  }
}

