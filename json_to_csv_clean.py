#!/usr/bin/env python3
import os, json, glob, argparse
import pandas as pd

def load_articles(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and isinstance(data.get('articles'), list):
        return data['articles']
    if isinstance(data, list):
        return data
    return []

def normalize(items):
    if not items:
        return pd.DataFrame()
    df = pd.json_normalize(items, sep='.')
    df = df.rename(columns={'source.id': 'source_id', 'source.name': 'source_name'})
    base_cols = ['source_name','source_id','author','title','description','url','urlToImage','publishedAt','content']
    for c in base_cols:
        if c not in df.columns:
            df[c] = pd.NA
    other = [c for c in df.columns if c not in base_cols]
    return df[base_cols + other]

def process(glob_pattern, out_dir, combined_name):
    files = sorted(glob.glob(glob_pattern))
    frames = []
    os.makedirs(out_dir, exist_ok=True)
    for fp in files:
        items = load_articles(fp)
        df = normalize(items)
        category = os.path.basename(fp).split('_')[0]
        df.insert(0, 'category', category)
        out_path = os.path.join(out_dir, os.path.splitext(os.path.basename(fp))[0] + '.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')
        frames.append(df)
    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined.to_csv(os.path.join(out_dir, combined_name), index=False, encoding='utf-8')

def main():
    p = argparse.ArgumentParser(description="Convert article JSON to CSV.")
    p.add_argument('--glob', default='*_articles_*.json', help='Input file glob')
    p.add_argument('--out', default='.', help='Output directory')
    p.add_argument('--combined', default='all_articles.csv', help='Combined CSV filename')
    args = p.parse_args()
    process(args.glob, args.out, args.combined)

if __name__ == '__main__':
    main()
