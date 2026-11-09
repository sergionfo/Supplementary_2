import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
INK = '#1f2a38'; FS = 7.6; BLUE = '#1f5fbf'
fig = plt.figure(figsize=(10.0, 7.9)); ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100); ax.set_ylim(-4, 75); ax.axis('off')

def box(x, y, w, h, t, kind='h', fs=FS, bold=False):
    fc, ec, ls, lw = {'h': ('white', INK, '-', 1.0), 'a': ('#e3eefc', BLUE, '-', 1.0),
                      'x': ('#f5f5f5', '#999', '--', 1.0), 'inc': ('#e3ebf4', INK, '-', 1.7)}[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=0.6', fc=fc, ec=ec, lw=lw, ls=ls))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs, color=INK, linespacing=1.18,
            weight='bold' if bold else 'normal')

def arr(p, q, ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9, mutation_scale=9, ls=ls))

# stage bars
for name, y, h in [('Identification', 58, 16), ('Screening', 40.5, 15.5), ('Eligibility', 29, 9.5), ('Included', 5, 21.5)]:
    ax.add_patch(FancyBboxPatch((0.5, y), 3.2, h, boxstyle='round,pad=0,rounding_size=0.6', fc=INK, ec=INK))
    ax.text(2.1, y + h / 2, name, rotation=90, ha='center', va='center', color='white', fontsize=FS, weight='bold')

MX, MW = 6, 36; RX, RW = 47, 24; OX, OW = 74, 25.5

# Identification
box(MX, 66.5, MW, 7.5, 'Records identified through database searching\n(February 2026; journal articles, English, 2020–2025)\nWeb of Science n = 426 · Scopus n = 401 · total n = 827')
box(OX, 58, OW, 16, 'Additional records identified through\nother sources (revision, 1–3 November 2026;\nnot added to the corpus)\n\nSentinel set: 16 eligible studies,\n14 retrieved by the queries\nWoS sensitivity query: n = 140, 49 eligible\nWoS update 2026 (preliminary): n = 122,\n59 eligible (Figures 11–13 only)', 'a', fs=FS - 0.4)
box(RX, 66.5, RW, 7.5, 'Citation searching\n(backward/forward snowballing):\nnot performed', 'x')
box(MX, 58, MW, 5.5, 'Records after duplicates removed\nn = 468', 'a')
box(RX, 58, RW, 5.5, 'Duplicates removed n = 359\n(automated, Bibliometrix\nmergeDbSources: same DOI or title)', 'a', fs=FS - 0.4)
arr((MX + MW / 2, 66.5), (MX + MW / 2, 63.5)); arr((MX + MW, 60.75), (RX, 60.75))

# Screening
box(MX, 47, MW, 7.5, 'Records screened on titles and abstracts\nn = 468\n(decisions by the authors; screeners and\nagreement not recorded)')
box(RX, 47, RW, 7.5, 'Records excluded n = 270\nEC1 185 · EC2 54 · EC3 7\nEC4 4 · EC5 11 · EC6 9')
box(OX, 40.5, OW, 14, 'Audit of excluded records (revision)\nrandom sample n = 40 (seed 1)\nlikely false exclusions: 2\n(≈5%; Wilson 95% CI 1.4–16.5%)\none reader with LLM assistance', 'a', fs=FS - 0.4)
arr((MX + MW / 2, 58), (MX + MW / 2, 54.5)); arr((MX + MW, 50.75), (RX, 50.75)); arr((RX + RW, 50.75), (OX, 50.75), ls=':')
box(RX, 40.5, RW, 5, 'Full-text eligibility assessment:\nnot performed', 'x')

# Eligibility
box(MX, 29.5, MW, 8.5, 'Sources of evidence assessed for eligibility\nn = 198\n(retained records re-checked against\nIC1–IC4 and EC1–EC6 during revision)')
box(RX, 31, RW, 5.5, 'Excluded n = 1 (EC2: classification\nof slope-failure signals,\nno phase picking)')
arr((MX + MW / 2, 47), (MX + MW / 2, 38)); arr((MX + MW, 33.75), (RX, 33.75))

# Included
box(MX, 16.5, MW, 10, 'Sources of evidence included in the mapping\nn = 197\nG1 models 79 · G2 applications 100\nG3 datasets 7 · G4 transfer learning / synthetic 11\n(18 boundary cases kept; sensitivity in Section 2.6)', 'inc')
box(RX, 17.5, RW, 8, 'Lexical coding of all 197 records\n(rule-based, automated;\nvalidation sample n = 30,\n82% of assignments correct)\n→ Table 17, Figures 14–15', 'a', fs=FS - 0.4)
arr((MX + MW / 2, 29.5), (MX + MW / 2, 26.5)); arr((MX + MW, 21.5), (RX, 21.5))
box(MX, 5.5, MW, 7.5, 'Sources of evidence charted from full text\n(purposive, most cited per group)  n = 33\nG1 14 · G2 14 · G3 2 · G4 3', 'inc')
box(RX, 5.5, RW, 7.5, 'Not read in full n = 164\n(bibliometric and lexical\nmapping only)')
arr((MX + MW / 2, 16.5), (MX + MW / 2, 13)); arr((MX + MW, 9.25), (RX, 9.25))

# legend
for i, (k, t) in enumerate([('h', 'step by the authors'), ('a', 'automated or AI-assisted step'),
                            ('x', 'recommended step, not performed'), ('inc', 'sources of evidence used in the synthesis')]):
    lx = [1, 23, 49, 76][i]
    box(lx, -2.9, 3, 1.5, '', k); ax.text(lx + 3.8, -2.15, t, va='center', fontsize=FS - 0.4, color=INK)
plt.savefig('/tmp/claude-0/w19/fig_prisma_scr.png', dpi=300)
print('ok')
