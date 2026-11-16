import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analysis as A


def test_real_scales_by_the_price_index():
    cpi = {2000: 50.0, 2025: 100.0}
    assert A.real(10.0, 2000, cpi) == 20.0
    assert A.real(10.0, 1970, cpi) is None


def test_gini_limits():
    assert A.gini([5, 5, 5, 5]) == 0
    assert abs(A.gini([0, 0, 0, 10]) - 0.75) < 1e-9


def test_split_counts_both_draws():
    out = A.split([dict(round='Champion', players_per_draw='1', prize_gbp='100'), dict(round='Qualifying first round', players_per_draw='64', prize_gbp='1')])
    assert out[0]['players'] == 2 and out[0]['paid'] == 200 and not out[0]['qualifying']
    assert out[1]['paid'] == 128 and out[1]['qualifying']


def test_the_2026_draw_adds_up_to_128_players_and_fits_inside_the_fund():
    sp = A.split(A.rows('wimbledon_2026_singles.csv'))
    assert sum(s['players'] for s in sp if not s['qualifying']) == 256
    total = [float(r['total_gbp']) for r in A.rows('wimbledon_prize_money.csv') if r['year'] == '2026'][0]
    assert sum(s['paid'] for s in sp) < total


def test_prize_series_has_no_2020_and_rises_over_the_long_run():
    years = [int(r['year']) for r in A.rows('wimbledon_prize_money.csv')]
    assert 2020 not in years and years == sorted(years) and years[0] == 1968 and years[-1] == 2026
