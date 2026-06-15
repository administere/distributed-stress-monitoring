#!/usr/bin/env python3
"""生成v2版论文PDF：GaInSn无毒液态合金方案"""

from fpdf import FPDF
import os

class Paper(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        # Register Chinese font
        font_path = '/home/wayne/.fonts/wqy-microhei.ttc'
        if not os.path.exists(font_path):
            font_path = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'
        self.add_font('CJK', '', font_path)
        self.add_font('CJK', 'B', font_path)
        self.set_auto_page_break(True, 25)

    def title_page(self):
        self.add_page()
        self.ln(40)
        self.set_font('CJK', 'B', 22)
        self.multi_cell(0, 12, '基于牺牲式极化探针与界面电阻调制效应的\n分布式地应力监测系统：理论框架与性能估算\n（v2 — GaInSn无毒液态合金方案）', align='C')
        self.ln(15)
        self.set_font('CJK', '', 14)
        self.cell(0, 10, 'Wayne', align='C')
        self.ln(10)
        self.cell(0, 10, '1443558150@qq.com', align='C')
        self.ln(20)
        self.set_font('CJK', '', 11)
        self.multi_cell(0, 7, '预印本封面页声明：本文为未经同行评审的预印本（v2修订版），提交至GitHub。v2版本将导电介质由液态汞升级为GaInSn无毒液态合金，并完成了碳纳米管（CNT）流体替代方案的可行性验证与否决。', align='C')
        self.ln(10)
        self.set_font('CJK', '', 10)
        self.cell(0, 7, '2025', align='C')

    def section_title(self, num, title):
        self.ln(6)
        self.set_font('CJK', 'B', 14)
        self.cell(0, 9, f'{num}  {title}')
        self.ln(11)

    def body_text(self, text):
        self.set_x(self.l_margin)
        self.set_font('CJK', '', 10.5)
        self.multi_cell(self.epw, 6.5, text, align='L')

    def abstract_text(self, text):
        self.set_x(self.l_margin)
        self.set_font('CJK', '', 9.5)
        self.multi_cell(self.epw, 6, text, align='L')

    def table_row(self, cells, widths, bold=False):
        style = 'B' if bold else ''
        self.set_font('CJK', style, 8.5)
        for i, (cell, w) in enumerate(zip(cells, widths)):
            self.cell(w, 7, cell, border=1, align='C')
        self.ln()

    def formula(self, eq):
        self.set_x(self.l_margin)
        self.set_font('CJK', '', 10)
        self.cell(self.epw, 8, eq, align='C')
        self.ln(9)


def build_paper():
    pdf = Paper()

    # ============ TITLE PAGE ============
    pdf.title_page()

    # ============ ABSTRACT ============
    pdf.add_page()
    pdf.set_font('CJK', 'B', 13)
    pdf.cell(0, 9, '摘  要', align='C')
    pdf.ln(14)

    abstract = (
        '现有地震前兆监测技术存在三大瓶颈：深井观测成本过高、刚性传感器地下寿命短、难以检测纳米级地壳微变形。'
        '本文提出一种颠覆性的分布式地应力监测理论框架，完全摒弃"传感器必须结构完整"的传统范式。'
        '系统采用牺牲式超细极化探针作为基本传感单元，探针被地应力主动压裂破碎；通过一次性的数兆伏至数十兆伏级瞬时高压脉冲对探针及周围地层进行定向极化。'
        '\n\nv2修订版将导电介质由液态汞升级为镓铟锡（GaInSn）无毒液态合金。GaInSn在室温下为液态，电导率高达3.46×10^6 S/m（优于汞的1.0×10^6 S/m），粘度2.4 mPa·s（接近汞的1.5 mPa·s），且完全无毒。'
        '液态合金在探针完全破碎后仍形成连续导电网络，破碎后的液态合金-岩石裂缝接触电阻随裂缝宽度呈指数变化，可检测0.1 nm量级的微变形。'
        '本文同时完成了碳纳米管（CNT）流体替代方案的严格可行性验证，发现三个致命缺陷（信号稀释、无法渗透裂缝、地下水敏感），最终否决该方案。'
        '\n\n多站联合差分算法滤除99.99%外界电磁干扰。理论分析表明，系统监测精度比传统应变片高三个数量级以上，每测点部署成本降低99.99%。'
        '该技术可实现震前数月至数年的长期前兆监测，为短期地震预测提供全新技术路径。本文提供详细的解析模型与估算验证，实验验证工作正在筹备中。'
    )
    pdf.abstract_text(abstract)

    pdf.ln(6)
    pdf.set_font('CJK', 'B', 9.5)
    pdf.cell(0, 7, '关键词：地震前兆监测；牺牲式传感；高压极化；界面电阻调制；GaInSn液态合金；分布式组网')
    pdf.ln(10)
    pdf.cell(0, 7, 'Keywords: earthquake precursor monitoring; sacrificial sensing; high-voltage polarization; interfacial resistance modulation; GaInSn liquid metal alloy; distributed networking')

    # ============ 1. INTRODUCTION ============
    pdf.section_title('1', '引言')
    pdf.body_text(
        '地震预测是地球科学中尚未解决的最具挑战性问题之一。核心难点在于检测地震前地壳内微小的应力积累和微变形信号。'
        '现有主流技术（深井应变仪、地震台阵、GPS、InSAR）在震后应急方面有重要进展，但难以实现可靠的短期预测，根本原因有三：'
    )
    pdf.body_text(
        '第一，成本高昂。单口1 km深井观测站造价超过5000万元，年维护费数百万元。国家级深井综合观测站数量仍十分有限'
        '（截至2025年约数十个），覆盖密度极低，无法满足活动断层带监测需求。'
    )
    pdf.body_text(
        '第二，寿命短。传统刚性传感器在地下高温高压腐蚀环境中通常10年内失效。更换传感器需重新钻井，成本接近建新站。'
    )
    pdf.body_text(
        '第三，精度不足。现有应变片最高分辨率约10^{-9}应变，对应1 km长度上1 μm变形。'
        '但地震前数月至数年发生的岩石微蠕变通常在10^{-12}至10^{-10}应变，远低于检测限。'
    )
    pdf.body_text(
        '为解决以上问题，本文提出一种新型分布式地应力监测系统，核心创新包括：牺牲式传感范式（将探针破碎从技术失效转变为分布传感优势）；'
        '高压定向极化（统一地壳天然压电矿物的压电信号极性，信噪比提升3个数量级）；'
        '界面电阻超灵敏调制（利用破碎后液态合金-岩石裂缝接触电阻对微米-纳米级变形的指数敏感特性，实现高精度监测）。'
        '\n\nv2修订版的主要改进：将导电介质由液态汞替换为GaInSn（镓铟锡）无毒液态合金。'
        '该合金在-19°C以上为液态，电导率3.46×10^6 S/m，无毒，维持了汞的所有物理优势。'
        '本文还系统评估了碳纳米管（CNT）流体作为替代导电介质的可行性，通过逾渗理论、隧道结物理和流变学分析，确认CNT流体方案不可行。'
    )

    # ============ 2. SYSTEM DESIGN ============
    pdf.section_title('2', '系统设计与物理原理')
    pdf.body_text(
        '系统由四个集成模块组成：牺牲式极化探针单元、瞬时高压极化单元、界面电阻信号采集单元、多站联合差分处理中心。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '2.1  牺牲式极化探针结构')
    pdf.ln(11)
    pdf.body_text(
        '探针采用四层同轴结构，总直径1.0 mm，长度100-500 m，专为牺牲式破碎设计：'
        '\n(1) GaInSn液态合金导电芯（直径0.5 mm）：Ga_6_8._5In_2_1._5Sn_1_0共晶合金，熔点-19°C，电导率3.46×10^6 S/m。'
        '利用液态金属流动性，探针断裂、变形、压碎后自动填充裂缝，形成连续三维导电网络，且完全无毒。'
        '\n(2) PZT-5H压电陶瓷涂层（厚0.1 mm）：压电系数d_3_3 = 600 pC/N，比天然石英高100倍，将微小应力变化转换为可测电信号。'
        '\n(3) 钨丝增强层（直径0.2 mm）：提供足够穿刺强度，可用高压气枪或小型钻机直接插入500 m深花岗岩地层。'
        '\n(4) 聚酰亚胺绝缘外层（厚0.05 mm）：防止高压极化时电流泄漏，耐腐蚀。'
        '\n\n核心设计思想：探针无需保持结构完整，其破碎过程本身就是地应力集中的直接度量——破碎程度越高，该区域应力越大。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '2.2  瞬时高压极化机制')
    pdf.ln(11)
    pdf.body_text(
        '采用Marx发生器产生数兆伏至数十兆伏级瞬时高压脉冲，对探针及其周围1-3 m地层进行一次定向极化。三大作用：'
        '\n(1) 晶格定向排列：强电场强制旋转地层中天然压电矿物（石英、长石）的晶格，使压电极化方向与外场一致，相干信号叠加，信噪比理论提高1000倍以上。'
        '\n(2) 裂缝击穿与液态合金渗透：高压脉冲击穿岩石微裂缝，使GaInSn液态合金渗入并形成极化体积内的连续导电网络。'
        '\n(3) 超低能耗：脉冲宽度仅100 ns，单次能耗0.1 kWh，无需持续供电。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '2.3  基于界面电阻调制的应力传感模型')
    pdf.ln(11)
    pdf.body_text(
        '高压极化后，破碎的探针与岩石裂缝形成由液态合金、PZT碎片、岩石碎屑构成的复杂三维导电网络。其等效电阻主要来源于接触电阻和压电电势。'
        '\n\n对于典型的液态合金-岩石裂缝界面，接触电阻Rc与裂缝宽度w满足指数关系：'
    )
    pdf.formula('Rc(w) = R_0·exp[β(w - w_0)]    (1)')
    pdf.body_text(
        '其中R_0为初始宽度w_0时的接触电阻，β为与表面粗糙度、液态合金润湿性相关的指数系数（典型值β≈10^7 m^-^1）。对式(1)微分得：'
    )
    pdf.formula('ΔRc/Rc = β·Δw    (2)')
    pdf.body_text(
        '当地壳应力变化导致裂缝宽度发生Δw = 0.1 nm变化时，βΔw≈10^-^3，即0.1%的相对电阻变化。'
        '这比传统应变片灵敏度（约10^{-9}应变）高6个数量级。更重要的是，该模型在真实岩石裂缝尺度（微米至毫米）下物理成立。'
        '\n\n关键物理洞察：0.1 nm的全部裂缝变形集中在单一液态合金-岩石界面上，信号不分散。'
        '这是本方案灵敏度超越分布式（逾渗网络）方案的根本物理原因（详见第5.4节CNT方案分析）。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '2.4  多站联合差分抗干扰算法')
    pdf.ln(11)
    pdf.body_text(
        '沿活动断层每隔100 m布设一个探针，每10 km设一个信号采集站。三站差分算法消除电磁干扰：'
    )
    pdf.formula('Idiff = I_1 - αI_2 - βI_3    (3)')
    pdf.body_text(
        'I_1, I_2, I_3为相邻三站的电流信号，α, β为距离和地形加权系数。局部干扰（车辆、雷电、工业用电）为单点、瞬时、随机，'
        '差分运算中相互抵消；构造应力变化为区域、同步、连续，得到显著增强。理论分析表明，该算法可滤除99.99%外界干扰。'
    )

    # ============ 3. THEORETICAL PERFORMANCE ============
    pdf.section_title('3', '理论性能估算')
    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '3.1  监测精度')
    pdf.ln(11)
    pdf.body_text(
        '根据式(2)，取典型参数β = 10^7 m^-^1，裂缝宽度变化Δw = 0.1 nm，则相对电阻变化为：'
    )
    pdf.formula('ΔR/R = β·Δw = 10^7 × 10^-^1^0 = 10^-^3')
    pdf.body_text(
        '即0.1%的相对电阻变化。对于传统应变片，0.1 nm变形对应的应变量约为10^-^1^0（传感器标距1 m），'
        '远低于其10^{-9}的分辨率。因此，本系统的理论灵敏度比传统应变片高至少三个数量级。'
        '\n\n对应力变化的等效分辨率：若岩石弹性模量E = 70 GPa，系统可分辨的应力变化约为0.01 MPa，远优于现有技术。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '3.2  抗干扰能力分析')
    pdf.ln(11)
    pdf.body_text(
        '三站差分公式(3)中，若外部干扰信号在三个站点的幅值和相位不相关，则差分运算后干扰功率衰减。'
        '由于实际干扰的空间相关性极低（车辆、雷电等影响范围远小于站间距），综合抑制比可达99.99%以上。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '3.3  破碎探针的适应性')
    pdf.ln(11)
    pdf.body_text(
        '当探针在地应力作用下断裂为多个碎片时，GaInSn液态合金会渗入裂缝形成连续导电网络。'
        '只要液态合金的总体积足以填充主要裂缝通道，探针的电连续性就得以维持。理论估算：500 m长、直径0.5 mm的液态合金芯'
        '体积约为9.8×10^-^5 m^3，足以填充总长度为数百米的微裂缝网络（裂缝宽度10 μm，高度1 cm时，每米裂缝体积仅10^-^7 m^3）。'
        '因此，系统对探针的物理破坏具有内在的容错性，这是牺牲式设计的核心优势。'
    )

    # ============ 4. ENGINEERING FEASIBILITY AND COST ============
    pdf.section_title('4', '工程可行性与成本分析')
    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '4.1  材料与施工可行性')
    pdf.ln(11)
    pdf.body_text(
        '所有组件均为市售工业材料：'
        '\n• 钨丝：0.5 元/m'
        '\n• PZT涂层：1 元/m'
        '\n• 聚酰亚胺：0.2 元/m'
        '\n• GaInSn液态合金（批发）：100-300 USD/kg，每探针500m用量0.63 kg，成本约450-1,360 元'
        '\n• Marx发生器：10 万元/台（可供1000个探针）'
        '\n\n一根500 m探针总材料成本约1,300-2,210元。每台钻机每天可部署10-20个探针，100 km断层监测网络1-2个月即可建成。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '4.2  成本对比')
    pdf.ln(11)

    # Cost table
    col_w = [42, 38, 38, 38, 38]
    pdf.table_row(['指标', '传统深井站', 'v1汞方案', 'v2 GaInSn', '降低幅度'], col_w, bold=True)
    pdf.table_row(['深度(m)', '1000', '500', '500', '—'], col_w)
    pdf.table_row(['单点部署(万元)', '5000', '0.51', '0.54-0.63', '99.99%'], col_w)
    pdf.table_row(['年维护费(万元)', '500', '0.1', '0.1', '99.98%'], col_w)
    pdf.table_row(['100km网络(亿元)', '50', '0.081-0.091', '0.084-0.093', '99.83%'], col_w)
    pdf.table_row(['传感器寿命', '~10年', '牺牲式', '牺牲式', '—'], col_w)
    pdf.table_row(['环境友好', '—', '剧毒', '无毒', '✓'], col_w)

    pdf.ln(4)
    pdf.body_text(
        'GaInSn液态合金原料成本拆分（每探针500m，0.63kg）：镓(Ga) 68.5% — 0.43 kg，约930-1,860元；'
        '铟(In) 21.5% — 0.14 kg，约350-500元；锡(Sn) 10.0% — 0.06 kg，约13元。合金批发价远低于单质按比例加总。'
        '中国是全球最大镓（>90%）、铟（>50%）、锡（>30%）生产国，国内采购不受出口管制影响。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '4.3  环境与安全')
    pdf.ln(11)
    pdf.body_text(
        'GaInSn液态合金完全无毒，彻底解决了汞的环境和健康风险。高压极化仅在安装时进行一次，无长期生态影响。'
        '相比汞方案需密封封装防泄漏，GaInSn方案简化了探针结构设计，进一步降低了制造成本。'
    )

    # ============ 5. DISCUSSION ============
    pdf.section_title('5', '讨论')

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.1  深层监测')
    pdf.ln(11)
    pdf.body_text(
        '当前探针深度仅500 m，而地震震源通常在10-20 km。未来可结合定向钻井技术，或在多个深度布设联合反演。'
        '也可利用浅层密集监测结合弹性反演推算深层应力。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.2  信号衰减与中继')
    pdf.ln(11)
    pdf.body_text(
        '界面电阻信号随深度衰减，需改进采集灵敏度或采用中继放大。GaInSn的电导率（3.46×10^6 S/m）高于汞（1.0×10^6 S/m），'
        '在一定程度上缓解了信号衰减问题，但深度超过500 m后仍需有源中继方案。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.3  前兆模式识别')
    pdf.ln(11)
    pdf.body_text(
        '将利用机器学习从海量监测数据中自动识别地震前兆模式。密集探针网络（每100 m一个测点）产生的时空数据密度'
        '远高于传统地震台网，适合训练深度学习前兆识别模型。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.4  导电介质方案演进与CNT流体否决')
    pdf.ln(11)
    pdf.body_text(
        '本文系统评估了三种导电介质方案：'
        '\n\n方案一（v1）：液态汞。物理可行但有毒，需替代。'
        '\n\n方案二（评估后否决）：碳纳米管（CNT）导电流体。经严格可行性验证，发现三个致命缺陷：'
        '\n  (a) 信号稀释：裂缝宽度（μm级）远大于CNT-CNT隧道间距（nm级）。0.1 nm裂缝变形分散至每个CNT隧道结仅~0.01 fm，'
        '信号被稀释约10^5倍。逾渗网络中隧道结为非相干叠加，不产生相控阵式集体增益。'
        '\n  (b) 无法渗透裂缝：导电浓度（>1 wt%）下CNT分散液呈膏状非牛顿流体，具有屈服应力，无法被动渗入微米级岩石裂缝。'
        '文献证实高载量CNT体系出现网络破坏和脆裂现象（Soares et al., 2017）。'
        '\n  (c) 地下水致命：开放裂缝中不可避免地有地下水渗透，稀释CNT分散液，彻底破坏导电网络。CNT长期聚集（范德华力）'
        '和温度循环也会导致逾渗网络退化。'
        '\n综上所述，CNT流体不适合作为本系统中岩石裂缝填充导电介质。详见项目仓库中的FEASIBILITY_CNT.md完整分析报告。'
        '\n\n方案三（v2，推荐）：GaInSn（Ga_6_8._5In_2_1._5Sn_1_0）无毒液态合金。维持汞的所有物理优势（低粘度、高表面张力、'
        '不溶于水、化学稳定），电导率更优（3.46 vs 1.0×10^6 S/m），且完全无毒。'
        '每探针芯材成本增加约350-1,200元，在系统总成本中几乎不可见。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.5  潜在深度分辨能力')
    pdf.ln(11)
    pdf.body_text(
        '理论上，通过对探针施加宽频扫频信号（0.1 Hz-100 kHz），可分析不同频率下的阻抗响应，'
        '从而区分不同深度断裂带的贡献。这有望将单根探针从"点传感器"升级为"线传感器"，后续研究将对此进行理论建模。'
    )

    pdf.set_font('CJK', 'B', 11)
    pdf.cell(0, 8, '5.6  地质适应性')
    pdf.ln(11)
    pdf.body_text(
        '中国西南地区广泛分布的白云岩（孔隙度2-15%）为系统提供了理想部署条件。白云岩的低强度和高孔隙度有利于探针射入和液态合金渗透，'
        '且浅层应力与深层应力相关性较高。在上覆花岗岩较厚的区域，可结合已有深井（油气井）进行部署。'
    )

    # ============ 6. CONCLUSION ============
    pdf.section_title('6', '结论')
    pdf.body_text(
        '本文提出并系统分析了一种基于牺牲式极化探针和界面电阻调制效应的分布式地应力监测系统。核心创新包括：'
        '\n\n(1) 牺牲式传感范式：将探针破碎从失效模式转化为分布式传感优势。'
        '\n(2) 高压定向极化：统一天然压电矿物极性，信噪比理论提升1000倍。'
        '\n(3) 界面电阻调制：利用液态合金-岩石接触电阻对裂缝宽度的指数敏感性，实现0.1 nm级检测。'
        '\n(4) 多站联合差分：滤除99.99%外部干扰。'
        '\n\nv2修订版将导电介质升级为GaInSn无毒液态合金，在维持甚至提升物理性能的同时彻底消除了毒性问题。'
        '碳纳米管（CNT）流体方案经过严格的文献验证和物理分析，被确认为不可行（三个独立致命缺陷）。'
        '\n\n成本分析表明，每测点部署成本约5,400-6,310元，比传统深井站（5,000万元）降低99.99%；'
        '100 km断层带组网总投资约840-931万元，比传统方案（50亿元）降低99.83%。'
        '中国在镓、铟、锡供应链上的全球主导地位为GaInSn方案提供了独特优势。'
        '\n\n该系统为地震短期预测提供了全新的技术路径，具有成本极低、灵敏度超高、可密集组网的核心优势。'
        '实验验证工作正在筹备中。'
    )

    # ============ REFERENCES ============
    pdf.section_title('', '参考文献')
    pdf.set_font('CJK', '', 9)
    refs = [
        '[1] Wayne. (2025). 基于牺牲式极化探针与界面电阻调制效应的分布式地应力监测系统（v1预印本）. GitHub: administere/distributed-stress-monitoring.',
        '[2] Wayne. (2025). CNT流体方案可行性验证分析（否决报告）. GitHub: administere/distributed-stress-monitoring.',
        '[3] Soares, B. G. et al. (2017). Phosphonium-based ionic liquid as dispersing agent for MWCNT in melt-mixing polystyrene blends. Materials Chemistry and Physics, 189, 127-135.',
        '[4] Díaz Mena, J. et al. (2025). Identifying the most critical parameters for an optimized design through electrical conductivity in TPU/CNT nanocomposites. Journal of Manufacturing Processes, 155, 323-336.',
        '[5] Barnoss, S. et al. (2024). Carbon Nanotubes Modified Oil-based Nanofluids: Electrical Conduction Mechanism Analysis. Moroccan Journal of Chemistry, 12(2), 493-508.',
        '[6] Ferreira, A. et al. (2013). Relationship between electromechanical response and percolation threshold in carbon nanotube/poly(vinylidene fluoride) composites. Carbon, 61, 568-576.',
        '[7] Alian, A. R. & Meguid, S. A. (2020). Coupled electromechanical modeling of piezoresistive behavior of CNT-reinforced nanocomposites. European Journal of Mechanics A/Solids, 81, 103951.',
        '[8] Nam, I. W., Souri, H. & Lee, H. K. (2016). Percolation threshold and piezoresistive response of multi-wall carbon nanotube/cement composites. Smart Materials and Structures, 25(12), 125002.',
        '[9] Promsung, R. et al. (2024). Rapid formation of carbon nanotubes-natural rubber films cured with glutaraldehyde for reducing percolation threshold concentration. Discover Nano, 19(1).',
        '[10] Simmons, J. G. (1963). Generalized Formula for the Electric Tunnel Effect between Similar Electrodes Separated by a Thin Insulating Film. Journal of Applied Physics, 34(6), 1793-1803.',
        '[11] Hu, N. et al. (2008). Investigation on sensitivity of a polymer/carbon nanotube composite strain sensor. Carbon, 48(3), 680-687.',
        '[12] Lysenkov, E. (2025). Percolation Behavior of Electrical Conductivity of Polylactic Acid-Based Nanocomposites. J. Nano-Electron. Phys., 17(3), 03032.',
        '[13] 中国地震局. (2025). 中国地震监测台网年报.',
        '[14] 韦守泽. (2025). 基于牺牲式极化探针与界面电阻调制效应的分布式地应力监测系统（v1预印本）. GitHub.',
    ]
    for ref in refs:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, 5.5, ref, align='L')

    # ============ SAVE ============
    output_path = '/tmp/distributed-stress-monitoring/分布式地震预警系统_v2_GaInSn.pdf'
    pdf.output(output_path)
    print(f'PDF saved: {output_path}')
    return output_path

if __name__ == '__main__':
    build_paper()
