"""Who gets paid at Wimbledon? Prize money since 1968, adjusted for inflation, and how the 2026 fund is split.

    python analysis.py        # reads data/, writes results/results.json

Uses only the Python standard library.
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRICE_YEAR = 2025


def rows(name):
    with open(HERE / 'data' / name, newline='') as f:
        return list(csv.DictReader(f))


def real(amount, year, cpi, to=PRICE_YEAR):
    """An amount from `year` in the prices of `to`. Returns None when there is no index for the year."""
    if year not in cpi or to not in cpi:
        return None
    return amount * cpi[to] / cpi[year]


def gini(values):
    """Gini coefficient: 0 when everyone gets the same, close to 1 when one person gets everything."""
    v = sorted(values)
    n, total = len(v), sum(v)
    if n == 0 or total == 0:
        return 0.0
    return sum((2 * (i + 1) - n - 1) * x for i, x in enumerate(v)) / (n * total)


def split(rounds, draws=2):
    """Money paid in each round of the singles, for both draws together."""
    out = []
    for r in rounds:
        n, prize = int(r['players_per_draw']), float(r['prize_gbp'])
        out.append(dict(round=r['round'], players=n * draws, prize=prize, paid=n * draws * prize, qualifying=r['round'].startswith('Qualifying')))
    return out


def main():
    cpi = {int(r['year']): float(r['cpi_2015_100']) for r in rows('uk_cpi.csv')}
    prize = [dict(year=int(r['year']), total=float(r['total_gbp']), men=float(r['mens_champion_gbp']), women=float(r['womens_champion_gbp'])) for r in rows('wimbledon_prize_money.csv')]
    for p in prize:
        p['total_real'] = real(p['total'], p['year'], cpi)
        p['men_real'] = real(p['men'], p['year'], cpi)
        p['champions_share'] = (p['men'] + p['women']) / p['total']
        p['women_to_men'] = p['women'] / p['men']
    by = {p['year']: p for p in prize}
    sp = split(rows('wimbledon_2026_singles.csv'))
    main_draw = [s for s in sp if not s['qualifying']]
    payouts = [s['prize'] for s in main_draw for _ in range(s['players'])]
    total_2026 = by[2026]['total']
    singles_main = sum(s['paid'] for s in main_draw)
    qualifying = sum(s['paid'] for s in sp if s['qualifying'])
    half = sorted(payouts)[:len(payouts) // 2]
    accounts = [dict(year=int(r['year']), turnover=float(r['turnover_gbp_m']), profit=float(r['profit_gbp_m']), lta=float(r['paid_to_lta_gbp_m']),
                     prize=by[int(r['year'])]['total'] / 1e6, prize_share=by[int(r['year'])]['total'] / 1e6 / float(r['turnover_gbp_m'])) for r in rows('aeltc_accounts.csv')]
    growth = {}
    for start in (1990, 2000, 2010, 2015):
        a, b = by[start], by[PRICE_YEAR]
        growth[start] = dict(nominal=b['total'] / a['total'], real=b['total'] / a['total_real'], champion_real=b['men'] / a['men_real'])
    slams = [dict(slam=r['slam'], currency=r['currency'], total=float(r['total']), champion=float(r['champion']), first_round=float(r['first_round']),
                  champion_to_first=float(r['champion']) / float(r['first_round']), champions_share=2 * float(r['champion']) / float(r['total'])) for r in rows('slams_2026.csv')]
    rg = [dict(year=int(r['year']), total=float(r['total_eur'])) for r in rows('roland_garros_prize_money.csv')]
    results = dict(
        price_year=PRICE_YEAR, prize=prize, cpi=cpi, growth=growth,
        split=sp, total_2026=total_2026, singles_main=singles_main, qualifying=qualifying, other=total_2026 - singles_main - qualifying,
        gini=round(gini(payouts), 4), bottom_half_share=round(sum(half) / singles_main, 4),
        champions_share_of_singles=round(2 * by[2026]['men'] / singles_main, 4),
        first_equal_year=min(p['year'] for p in prize if p['women'] == p['men']),
        accounts=accounts, slams=slams, roland_garros=rg,
    )
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results' / 'results.json').write_text(json.dumps(results, separators=(',', ':')) + '\n')
    print({k: results[k] for k in ('growth', 'singles_main', 'qualifying', 'other', 'gini', 'bottom_half_share', 'champions_share_of_singles', 'first_equal_year', 'accounts')})
    print([(s['slam'], round(s['champion_to_first'], 1), round(s['champions_share'], 3)) for s in slams])
    print([(y, round(by[y]['champions_share'], 3), round(by[y]['women_to_men'], 2)) for y in (1968, 1980, 1990, 2000, 2007, 2015, 2026)])


if __name__ == '__main__':
    main()
