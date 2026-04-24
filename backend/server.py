import asyncio
import base64
import hashlib
import os
import secrets
import time

import numpy as np
import pandas as pd
import pysam
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI(
    title="SCON API",
    version="1.0.0",
    root_path="/api/v1"
)

origins = []

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#df_meta = pd.concat([pd.read_csv('./data/scon_output_meta.csv'),
#                    pd.read_csv('scon_outputs/scon_output_meta.csv')]).sort_values(['species', 'ensemble_rev'])
df_meta_magr = pd.read_csv('./data/scon_magr_outputs/scon_output_meta.csv').sort_values(['species', 'ensemble_rev']) 
#col.names = species, grcm_ver, ensemble_rev, scon_file
df_meta_magr['label']=df_meta_magr.apply(lambda x: f"{x.species} {x.grcm_ver} (v.{x.ensemble_rev}) ", axis=1)
df_meta_magr['group_label']=df_meta_magr.apply(lambda x: f"Ensemble ver: {x.ensemble_rev}", axis=1) 

df_meta_vdgn = pd.read_csv('./data/scon_vdgn_outputs/scon_output_meta.csv').sort_values(['species', 'ensemble_rev']) 
# #col.names = species, grcm_ver, ensemble_rev, scon_file
df_meta_vdgn['label']=df_meta_vdgn.apply(lambda x: f"{x.species} {x.grcm_ver} (v.{x.ensemble_rev}) ", axis=1)
df_meta_vdgn['group_label']=df_meta_vdgn.apply(lambda x: f"Ensemble ver: {x.ensemble_rev}", axis=1) 
#col.names = species, grcm_ver, ensemble_rev, scon_file, label, group_label
#group_label = ensemble ver


def get_group_items(df):
    return df.apply(lambda x: x.to_dict(), axis=1).tolist()


def load_scon_data(scon_file, type:str):
    if (type == "VDGN"):
        print(f'./data/scon_vdgn_outputs/{scon_file}')
        df_scon = pd.read_parquet(f'./data/scon_vdgn_outputs/{scon_file}')
        print(df_scon.shape)
    else:
        print(f'./data/scon_magr_outputs/{scon_file}')
        df_scon = pd.read_parquet(f'./data/scon_magr_outputs/{scon_file}')
        print(df_scon.shape)
    # df_scon = pd.read_parquet('./data/scon_output.MAGR.parquet')
    df_scon.Exon_usage=df_scon.Exon_usage.fillna(0).astype(int)
    df_scon.GC=df_scon.GC.fillna(0).astype(int)
    return df_scon

@app.get('/meta/dataset')
#from metadata
async def list_dataset(type: str, species: str = None):
    if (type == 'MAGR'):
        df_meta = df_meta_magr
    else:
        df_meta = df_meta_vdgn

    if species:
        tmp=df_meta.query(f'species=="{species}"')
    else:
        tmp=df_meta
    
    if tmp.empty:
        return []
    datasets = [{'key': row.ensemble_rev,
                 'ensemble_rev': row.ensemble_rev,
                 'name': f'{row.grcm_ver} (Ensemble release {row.ensemble_rev})',
                 'dataset': row.scon_file,
                 'species': row.species,
                } for _, row in tmp.iterrows()]
    return datasets


@app.get('/sconable_genes')
#from metadata of scon_file.Gene
#SCON run search
async def sconable_genes(species: str, ensemble_rev: int, type:str):
    if (type == 'MAGR'):
        df_meta = df_meta_magr
    else:
        df_meta = df_meta_vdgn
    df_row = df_meta.query(f'species=="{species}" and ensemble_rev=={ensemble_rev}')
    if df_row.empty:
        return []
    scon_file = df_row.scon_file.iloc[0]
#     scon_sites = df_scon.query(f'scon_file=="{scon_file}"')
    scon_sites = load_scon_data(scon_file, type)
    return [{'name':x, 'code':x} for x in sorted(set(scon_sites.Gene))]

@app.get('/sconable_sites_group')
#PAM position grouping
async def sconable_sites_group(species: str, ensemble_rev: int, gene: str, type: str):
    if (type == 'MAGR'):
        df_meta = df_meta_magr
    else:
        df_meta = df_meta_vdgn
    df_row = df_meta.query(f'species=="{species}" and ensemble_rev=={ensemble_rev}')
    if df_row.empty:
        return []
    scon_file = df_row.scon_file.iloc[0]
    df_scon = load_scon_data(scon_file, type)

    scon_sites = df_scon.query(f'scon_file=="{scon_file}" and Gene=="{gene}"')
    scon_sites= scon_sites.replace([np.nan], [None])
    
    scon_gene = scon_sites#.eval('id=index')
    scon_gene['id'] = "scon." + scon_sites.Chromosome + "." + scon_sites.Insertion_start.astype(str)
    #return scon_gene.to_dict(orient='records')
    def to_dict(df):        
        row = df.iloc[0].to_dict()
        # cols = 'Gene Chromosome PAM_position Target_length Tartget_start Tartget_end Target_sequence'.split()
        # row['scon_sites']=df[cols+['id']].to_dict(orient='records')
        row['n_editable']=len(df)
        row['scon_sites']=df.to_dict(orient='records')
        return row
    
    cols = 'Gene Chromosome Transcript Exon Exon_usage Exon_size Exon_strand Exon_start Exon_end Insertion_start Insertion_end'.split()
    rows = [to_dict(df) for k, df in scon_gene.groupby(cols)]
#     rows = [k for k, df in scon_gene.groupby(cols)]
    
    return rows


@app.get('/sconable_site_count_by_transcript')
#Exon - Transcipt all count (+pam)
#SCONable site
async def sconable_site_count_by_transcript(species: str, ensemble_rev: int, gene: str, type:str):
    if (type == 'MAGR'):
        df_meta = df_meta_magr
    else:
        df_meta = df_meta_vdgn
    df_row = df_meta.query(f'species=="{species}" and ensemble_rev=={ensemble_rev}')
    if df_row.empty:
        return []

    scon_file = df_row.scon_file.iloc[0]
    df_scon = load_scon_data(scon_file, type)

    scon_sites = df_scon.query(f'scon_file=="{scon_file}" and Gene=="{gene}"')
    if scon_sites.empty:
        return []

    ts_meta = scon_sites[['Transcript', 'transcript_length', 'is_canonical']].drop_duplicates()

    ts_meta = ts_meta.replace([np.nan], [None])
    transcripts_metadata = ts_meta.to_dict(orient='records')

    scon_site_counts = scon_sites.groupby(['Transcript', 'Exon']).count().Gene.unstack(level=0)
    df_out = scon_site_counts.reset_index().replace(np.nan, None)

    return {'columns':df_out.columns.to_list(), 'rows': df_out.to_dict(orient='records'),'transcripts_metadata': transcripts_metadata}


@app.get('/scon_sites_by_transcript')
#seq data
async def scon_sites_by_transcript(species: str, ensemble_rev: int, exon: str, transcript: str, type: str):
    if (type == 'MAGR'):
        df_meta = df_meta_magr
    else:
        df_meta = df_meta_vdgn
    df_row = df_meta.query(f'species=="{species}" and ensemble_rev=={ensemble_rev}')
    if df_row.empty:
        return []
    

    scon_file = df_row.scon_file.iloc[0]
    if (type == 'MAGR'):
        scon_output = f'./data/scon_magr_outputs/{scon_file}'
    else:
        scon_output = f'./data/scon_vdgn_outputs/{scon_file}'
    gtf_file = f'./data/ref_data/{scon_file.replace(".SCON_DB.parquet", "")}'
    gtf_summary = f'{gtf_file}.summary.parquet'
    fasta_file = f'{gtf_file.replace(f".{ensemble_rev}.gtf", ".dna.toplevel.fa")}'


    df_scon=pd.read_parquet(scon_output)
    df_scon['scon_id'] = "scon." + df_scon.Chromosome + "." + df_scon.Insertion_start.astype(str)

    ref_fasta = pysam.FastaFile(fasta_file)
    scon_seq_info = pd.read_parquet(gtf_summary)

    scon_sites = df_scon.query(f'(Transcript=="{transcript}")&Exon=="{exon}"')
    # gene_info = scon_seq_info.query(f'gene_name=="{gene_name}"')
    gene_info = scon_seq_info.query(f'(feature=="exon")&(exon_id=="{exon}")')

    if scon_sites.empty or gene_info.empty:
        return []


    # gene = gene_info.query('feature=="gene"').iloc[0]
    gene = gene_info.iloc[0]
    print(f"Exon info: {gene}")
    
    # 1. 양방향 300bp 패딩 추가 (상동성 암 250bp + 여유분)
    PADDING_BP = 300
    fetch_start = max(0, gene.start - 1 - PADDING_BP) # 0 이하로 내려가는 것 방지
    fetch_end = gene.end + PADDING_BP

    gene_seq = ref_fasta.fetch(gene.chrom, fetch_start, fetch_end)

    # pysam fetch의 시작점은 0-based이므로, 실제 가져온 첫 염기의 유전체 좌표(1-based)
    genomic_start = fetch_start + 1

    # 2. 프론트엔드 UI(100bp 단위 정렬)를 위한 패딩 계산
    len_padding = 0 if (genomic_start % 100 == 0) else genomic_start % 100
    gene_seq = ' ' * len_padding + gene_seq

    # 3. bases 딕셔너리 생성 시 좌표 매핑 범위 수정
    bases = {i: {'chrom': gene.chrom, 'pos': i, 'base': c, 'className': 'dna-char'}
             for c, i in zip(gene_seq, range(genomic_start - len_padding, fetch_end + 1))}

    # 4. UI 그리드용 클래스 추가 루프 범위 수정
    for i in range(genomic_start - len_padding, fetch_end + 1):
        if i % 100 == 99:
            bases[i]['className'] += ' line-break'
        elif i % 50 == 49:
            bases[i]['className'] += ' chunk-sep-sep'
        elif i % 10 == 9:
            bases[i]['className'] += ' chunk-sep'

    for _, exon in gene_info.query('feature=="exon"').iterrows():
        for i in range(exon.start, exon.end+1):
            bases[i]['className'] += ' exon'

    def get_range(start, end):
        if start<end:
            return (start, end+1)
        return (end, start+1)

    for _, scon_site in scon_sites.iterrows():
        scon_idx = scon_site.scon_id
        for i in range(*get_range(scon_site.Insertion_start, scon_site.Insertion_end)):
            bases[i]['className'] += f' scon scon_MAGR {scon_idx}'
            bases[i]['sconIndex']= scon_idx

        for i in range(*get_range(scon_site.Tartget_start, scon_site.Tartget_end)):
            bases[i]['className'] += f' targetX {scon_idx}'
            bases[i]['sconIndex']= scon_idx


        if scon_site.PAM_position == 'left':
            # for i in range(scon_site.Tartget_start, scon_site.Tartget_start+3):
            for i in range(*get_range(scon_site.Tartget_start, scon_site.Tartget_start)):
                bases[i]['className'] += ' left-pam'
        elif scon_site.PAM_position == 'right':
            # for i in range(scon_site.Tartget_end-2, scon_site.Tartget_end+1):
            for i in range(*get_range(scon_site.Tartget_start, scon_site.Tartget_start)):
                bases[i]['className'] += ' right-pam'


    for i, x in bases.items():
        x['className'] = ' '.join(list(set(x['className'].split())))

    seqs = [x for i, x in bases.items()]

    return seqs
