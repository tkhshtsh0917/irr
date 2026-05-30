from pathlib import Path

import pandas as pd
from irrCAC.raw import CAC


def main(file_path: Path) -> None:
    # 1. Excelから評価データの読み込み
    # ※ 行: サンプル(200行) | 列: 評価者(6〜7列) | 値: 1〜5 の数値
    df = pd.read_excel(file_path, engine="calamine")

    # 評価者の列（例: rater1, rater2, ...）だけを抽出
    rater_data = df.filter(like="rater")

    # 2. 一致度計算オブジェクトの作成（順序尺度の重み付き(weights='ordinal')で計算）
    cac = CAC(rater_data, weights="ordinal")

    # 3. 各種指標を計算
    ac2_res = cac.gwet()
    alpha_res = cac.krippendorff()
    kappa_res = cac.fleiss()

    # 4. 信頼性係数の数値を抽出
    ac2_val = ac2_res["est"]["coefficient_value"]
    alpha_val = alpha_res["est"]["coefficient_value"]
    kappa_val = kappa_res["est"]["coefficient_value"]

    # 5. レポート出力
    print("==========================================")
    print("     評価者間一致度（IRR）分析レポート    ")
    print("==========================================")
    print(f"■ サンプル数  : {len(df)} 件")
    print(f"■ 評価者数    : {rater_data.shape[1]} 名")
    print("■ 採用尺度    : 5段階 順序尺度（Ordinal）")
    print("------------------------------------------")
    print(f"📊 Gwet's AC2             : {ac2_val:.4f} (★本命指標)")
    print(f"📊 Krippendorff's Alpha   : {alpha_val:.4f} (★世界標準・欠損対応)")
    print(f"📊 Fleiss' Kappa (Weighted): {kappa_val:.4f} (参考用ベンチマーク)")
    print("==========================================")


if __name__ == "__main__":
    file_path = Path("evaluation_data.xlsx")  # Excelファイルのパスを指定
    main(file_path)
