# %%
##SCONDB_Final_v2
#Add RightWing Case
#Modify Screening strategy
#Add Self-complementarity
##SCONDB_Final_v3


#Check APPRIS vs Ensembl
###########################################################
# Initiating SCONable Exon DB
##########################################################
import itertools
import re
import sys
import pandas as pd

#Required files
version = sys.argv[1]
species_version = sys.argv[2]

if species_version is None:
    species_version = 'Mus_musculus.GRCm38.102.gtf'
canonical_checking = True
#work_dir = '/data/analysis/leeheetak/0_SCON/SCON/'
work_dir = '.'
data_dir = f"../scon_inputs"

# %%
###########################################################################
# 1. Initiating analysis
###########################################################################
#--Setting utilities
#--Importing sequence info
#---Parsing fasta header and sequences
def is_header(line):
    call = False
    if line[0] == '>':
        call = True
    else: pass
    return call

def parse_header_seq(file_name):
    with open(file_name, 'r') as fa:
        data = fa.readlines()
        for header, group in itertools.groupby(data, key=is_header):
            group = list(group)
            if header:         
                head = list(group)[0].strip('\n')
            else:                                        
                sequence = ''.join(line.strip('\n') for line in list(group))
                yield head, sequence

#---Parsing exon info and sequences
def transform_str(a):        
    if a.isdigit(): 
        val = int(a)
    elif a.startswith('-') and a[1:].isdigit():
        val = int(a[1:])*(-1)
    else:
        val = a
    return val

def parse_exon_info(exon_file): #from exon_info_GRCm38.p6.txt
    '''
    Exon stable ID
    Constitutive exon
    Exon region start (bp)
    Exon region end (bp)
    Strand
    '''        
    head_seq = dict(parse_header_seq(exon_file))   
    e_seq = dict() 
    e_usage = dict()    
    e_region = dict()        
    e_strand = dict()    
    for head in head_seq.keys():                
        Head = [transform_str(e) for e in head[1:].split('|')] 
        ID, USAGE, START, END, STRAND = Head
        e_seq[ID] = head_seq[head]
        e_usage[ID] = USAGE
        e_region[ID] = (START, END)
        e_strand[ID] = STRAND
    return e_seq, e_usage, e_region, e_strand

#---Parsing Exon-Transcript relationships
def parse_exon_transcript_info(exon_transcript_file):    
    '''
    Gene name
    Chromosome
    Transcript ID
    Exon ID
    Strand
    '''       
    blacklist = ['']
    with open(exon_transcript_file) as fe:
        data = fe.readlines()
    fe.close()
    t_gene = dict()
    t_e_entry = dict()
    g_chromosome = dict()
    g_transcript = dict()
    for line in data:
        NAME, CHR, T_ID, E_ID, STRAND = [transform_str(e) for e in line.strip().split(',')]
        if NAME not in blacklist:
            t_gene[T_ID] = NAME
            g_chromosome[NAME] = CHR
            if NAME not in g_transcript.keys():
                g_transcript[NAME] = {T_ID:None}
            else: g_transcript[NAME][T_ID] = None
            if T_ID not in t_e_entry.keys():
                t_e_entry[T_ID] = {E_ID:None}
            else: t_e_entry[T_ID][E_ID] = None
        else: pass
    return t_gene, t_e_entry, g_chromosome, g_transcript

#---Parsing Transcript info
def curate_multiple_utr(utr, start_end):
    if type(utr) == type(''):
        if utr == '':
            fin_utr = '-'
        else:
            if start_end == 'start':
                fin_utr = min([transform_str(e) for e in utr.split(';')])
            else:
                fin_utr = max([transform_str(e) for e in utr.split(';')])       
    else: fin_utr = utr    
    return fin_utr

def parse_transcript_info(transcript_file):
    '''
    cDNA sequences
    5‘ UTR start
    5‘ UTR end
    3‘ UTR start
    3‘ UTR end
    Transcript stable ID
    Strand
    '''            
    head_seq = dict(parse_header_seq(transcript_file))  
    t_utr = dict()    
    t_strand = dict()   
    t_coding_length = dict() 
    for head in head_seq.keys():                
        Head = [transform_str(e) for e in head[1:].split('|')] 
        START5, END5, START3, END3, ID, STRAND = Head        
        START5 = curate_multiple_utr(START5, 'start')
        END5 = curate_multiple_utr(END5, 'end')
        START3 = curate_multiple_utr(START3, 'start')
        END3 = curate_multiple_utr(END3, 'end')
        t_utr[ID] = [START5, END5, START3, END3]
        t_strand[ID] = STRAND            
        t_coding_length[ID] = len(head_seq[head])
    return t_utr, t_strand, t_coding_length

def parse_putative_canonical_transcript():
    gene_coding_length = dict()
    gene_canonical_transcript = dict()
    for gene in g_transcript.keys():
        gene_coding_length[gene] = dict()
        gene_canonical_transcript[gene] = dict()    
    for gene in g_transcript.keys():        
        for transcript in g_transcript[gene].keys():
            if transcript in t_coding_length.keys():
                Length = t_coding_length[transcript]
                if Length not in gene_coding_length.keys():
                    gene_coding_length[gene][Length] = [transcript]
                else:
                    gene_coding_length[gene][Length].append(transcript)
            else: pass
    for gene in gene_coding_length.keys():
        if len(gene_coding_length[gene].keys()) > 0:
            target_length = max(list(gene_coding_length[gene].keys()))
            target_transcripts = list(set(gene_coding_length[gene][target_length]))
            for T_ID in target_transcripts:
                gene_canonical_transcript[gene][T_ID] = None
        else: del gene_canonical_transcript[gene]
    return gene_canonical_transcript

def canonical_transcript_info(canonical_transcript_file, canonical_checking):  
    gene_canonical_transcript = dict()  
    if canonical_checking:    
        with open(canonical_transcript_file) as fi:
            data = fi.readlines()
        fi.close()    
        for line in data:
#             gene, g_id, t_id, ccds, prin = line.strip().split('\t')
            gene, g_id, t_id, ccds, prin = line.replace('\n','').split('\t')
            if prin == 'PRINCIPAL:1': #PRINCIPAL:1 to PRINCIPAL:5
                if gene not in gene_canonical_transcript.keys():
                    gene_canonical_transcript[gene] = {t_id:None}
                else: gene_canonical_transcript[gene][t_id] = None
    else: gene_canonical_transcript = parse_putative_canonical_transcript()
    return gene_canonical_transcript

############################################# 
#2. CRISPR Targetable regular expression
############################################# 
# For reverse sequences
def generate_opposite_strand(seq):
    reverse_dict = {'A':'T', 'G':'C', 'T':'A', 'C':'G', 'N':'N', '.':'.', '(':')', ')':'(', '|':'|'}   
    seq_r = ''
    try:
        for s in seq: 
            seq_r += reverse_dict[s]    
    except:
        return None
    return seq_r[::-1]

def gccontent(seq):
    #print (seq)
    gc = round((seq.count('C') + seq.count('G'))/len(seq),3)*100
    return gc

#Check Self complementrarity
def add_stem_score(non_pam_seq):        
    backbone_regions = ["AGGCTAGTCCGT"]
    STEM_LEN = 4
    fwd = non_pam_seq
    rvs = generate_opposite_strand(non_pam_seq)
    if not rvs:
        return None
    L = len(fwd)-4-1
    folding = 0
    for i in range(0,len(fwd)-STEM_LEN):
        if gccontent(fwd[i:i+STEM_LEN]) >= 0.5:
            if fwd[i:i+STEM_LEN] in rvs[0:(L-i)] or any([fwd[i:i+STEM_LEN] in item for item in backbone_regions]):                    
                folding += 1
    return folding

def find_sconable_site_on_exon(exon, region, sequence_e):  
    #getting exon info.
    start_e, end_e = region
    strand = e_strand[exon]
#     strand = exon_profile[exon][3]
    #Insert site
    if version == 'vdgn':
        insert_list = [p1+p2+'G'+p4 for p1 in ['C', 'A', 'G'] for p2 in ['A','T','G'] for p4 in ['A', 'T', 'G', 'C']]
    else:
        insert_list = [p1+p2+'G'+p4 for p1 in ['C', 'A'] for p2 in ['A'] for p4 in ['A', 'G']]
    insert_result = {insert:[] for insert in insert_list}
    for insert in insert_result.keys():  
        matches = re.finditer(r'(?=({insert}))'.format(insert=insert), sequence_e)        
        if matches:
            for match in matches:                    
                match_start, match_end = match.start(1), match.end(1) - 1                
                if strand == 1:
                    match_genome_start, match_genome_end = start_e + match_start, start_e + match_end
                    insert_result[insert].append((match_start, match_end, match_genome_start, match_genome_end))
                else: 
                    match_genome_start, match_genome_end = end_e - match_end, end_e - match_start
                    insert_result[insert].append((match_start, match_end, match_genome_start, match_genome_end))            
        else: pass    
    #PAM sequence
    fin_result = list()
    #-PAM right - CAGA(NNNN)NGG
    for insert in insert_result.keys():
        if insert[-1] == 'G': 
            Range = [i for i in range(-1, 13)]
        else: 
            Range = [i for i in range(0, 13)]
        for ms, me, mgs, mge in insert_result[insert]:     
            if ms+23 < len(sequence_e):       
                screening_seq = sequence_e[ms:ms+23]
                match_pams = re.finditer(r'(?=(.GG))', screening_seq)           
                if match_pams:
                    for match_pam in match_pams:
                        match_pam_s, match_pam_e = match_pam.start(1), match_pam.end(1) - 1
                        new_ms, new_me = 0, 3                        
                        length_between = match_pam_s - new_me #CAGA(NNN..N)GG                       
                        if length_between in Range:
                            temp_length = match_pam_e + 1
                            extend = 23 - temp_length
                            if ms > extend - 1:
                                fin_s, fin_e = ms-extend, match_pam_e + ms
                                fin_seq = sequence_e[fin_s:fin_e+1]
                                non_pam_seq = fin_seq[:-3]
                                fold_sc = add_stem_score(non_pam_seq)
                                if strand == 1:
                                    fin_res = (insert, mgs, mge, 'right', fin_seq, non_pam_seq, fold_sc, (start_e+fin_s, start_e+fin_e))                            
                                else:
                                    fin_res = (insert, mgs, mge, 'right', fin_seq, non_pam_seq, fold_sc, (end_e-fin_e, end_e-fin_s))                                     
                                fin_result.append(fin_res)
                            else: pass                        
                        else: pass
                else: pass
            else: pass
    #-PAM left (out) - CAGA.....CCN(guide)
    for insert in insert_result.keys():
        if insert != '': 
            Range = [i for i in range(4, 13)] # y-x , when x is insert start, y is pam start
        else: pass
        for ms, me, mgs, mge in insert_result[insert]:     
            if ms+35 < len(sequence_e):       
                screening_seq = sequence_e[ms:ms+23]
                match_pams = re.finditer(r'(?=(CC.))', screening_seq)           
                if match_pams:
                    for match_pam in match_pams:
                        passing = False
                        match_pam_s, match_pam_e = match_pam.start(1), match_pam.end(1) - 1
                        new_ms, new_me = 0, 3                        
                        length_between = match_pam_s - new_ms #CAGA(NNN..N)CCN                      
                        if length_between in Range:
                            passing = True
                            if passing:
                                idx_pam_s = match_pam_s + ms                            
                                fin_s = idx_pam_s ##This is y
                                fin_e = idx_pam_s + 22 
                                fin_seq = sequence_e[fin_s:fin_e+1]                                
                                non_pam_seq = fin_seq[3:]
                                fold_sc = add_stem_score(non_pam_seq)
                                if strand == 1:
                                    fin_res = (insert, mgs, mge, 'left', fin_seq, non_pam_seq, fold_sc, (start_e+fin_s, start_e+fin_e))                            
                                else:
                                    fin_res = (insert, mgs, mge, 'left', fin_seq, non_pam_seq, fold_sc, (end_e-fin_e, end_e-fin_s))                                     
                                fin_result.append(fin_res)
                            else: pass                        
                        else: pass
                else: pass
            else: pass
    #-PAM left - CCN(NNNN)CAGA
    for insert in insert_result.keys():
        if insert[0] == 'C': 
            Range = [i for i in range(-1, 13)] 
        else: 
            Range = [i for i in range(0, 13)] 
        for ms, me, mgs, mge in insert_result[insert]:   
            if me > 21:         
                screening_seq = sequence_e[me-22:me + 1]
                match_pams = re.finditer(r'(?=(CC.))', screening_seq)
                if match_pams:
                    for match_pam in match_pams:
                        match_pam_s, match_pam_e = match_pam.start(1), match_pam.end(1) - 1
                        new_ms, new_me = 19, 22
                        length_between = new_ms - match_pam_e #CC(NNNN)CAGA                       
                        if  length_between in Range:
                            temp_length = len(screening_seq)- 1 - match_pam_s + 1
                            extend = 23 - temp_length
                            if extend > -1:
                                fin_s, fin_e = me - temp_length +1, me + extend
                                fin_seq = sequence_e[fin_s:fin_e+1]
                                non_pam_seq = fin_seq[3:]
                                fold_sc = add_stem_score(non_pam_seq)
                                if strand == 1:
                                    fin_res = (insert, mgs, mge, 'left', fin_seq, non_pam_seq, fold_sc, (start_e+fin_s, start_e+fin_e))                            
                                else:
                                    fin_res = (insert, mgs, mge, 'left', fin_seq, non_pam_seq, fold_sc, (end_e-fin_e, end_e-fin_s))                                      
                                fin_result.append(fin_res)
                            else: pass                        
                        else: pass            
                else: pass
            else: pass
    #-PAM right (out) - (guide)NGG....CAGA
    for insert in insert_result.keys():
        if insert != '': 
            Range = [i for i in range(3, 10)] # x-y , when x is insert start, y is pam start
        else: pass
        for ms, me, mgs, mge in insert_result[insert]:   
            if me > 36:         
                screening_seq = sequence_e[me-22:me + 1]
                match_pams = re.finditer(r'(?=(.GG))', screening_seq)
                if match_pams:
                    for match_pam in match_pams:
                        passing = False
                        match_pam_s, match_pam_e = match_pam.start(1), match_pam.end(1) - 1
                        new_ms, new_me = 19, 22
                        length_between = new_ms - match_pam_s #CC(NNNN)CAGA                       
                        if length_between in Range:
                            passing = True
                            idx_pam_s = match_pam_s + me - 22
                            if passing:  
                                fin_s = idx_pam_s-20
                                fin_e = idx_pam_s+2                       
                                fin_seq = sequence_e[fin_s:fin_e+1]                                
                                non_pam_seq = fin_seq[:-3]
                                fold_sc = add_stem_score(non_pam_seq)
                                if strand == 1:
                                    fin_res = (insert, mgs, mge, 'right', fin_seq, non_pam_seq, fold_sc, (start_e+fin_s, start_e+fin_e))                            
                                else:
                                    fin_res = (insert, mgs, mge, 'right', fin_seq, non_pam_seq, fold_sc, (end_e-fin_e, end_e-fin_s))                                      
                                fin_result.append(fin_res)
                            else: pass                        
                        else: pass            
                else: pass
            else: pass
    fin_result = list(set(fin_result))
    return fin_result


def exon_filter_1(transcript):
    '''
    5'st        5'end             3'st            3'end for forward
    3'end       3'st              5'end           5'start for reverse
    |////UTR/////||-----------------||/////UTR///////|
       |---|    |------|    |----| |--------|    |--|  Exons
                  |----|    |----| ||                  Coding_exon_regions
    '''
    exon_entry = [(exon, e_region[exon][0], e_region[exon][1]) for exon in t_e_entry[transcript].keys()]
    entry_exon_sort_start = sorted(exon_entry, key = lambda x: x[1])
    utr_info = t_utr[transcript]
    strand = t_strand[transcript]    
    fin_exon_entry = list()
    fin_exon_coding_seq = dict()      
    if utr_info.count('-') == 0: #both 5 and 3 prime utrs
        a, b, c, d = sorted(utr_info)    
        temp_start = b + 1
        temp_end = c - 1           
    elif utr_info.count('-') == 2 and utr_info[0] == '-': # ['-', '-', 3st/5end, 3end/5st]
        temp_start = entry_exon_sort_start[0][1]
        temp_end = utr_info[2] - 1     
    elif utr_info.count('-') == 2 and utr_info[2] == '-': # [5st/3end, 5end/3st, '-', '-']
        temp_start = utr_info[1] + 1
        temp_end = entry_exon_sort_start[-1][2]
    else:
        temp_start = entry_exon_sort_start[0][1]
        temp_end = entry_exon_sort_start[-1][2]
    set_transcript = set([i for i in range(temp_start, temp_end + 1)])    

    #Find overlap between non-utr-transcript and exon region
    transcript_coding_length = 0
    for exon, start_e, end_e in entry_exon_sort_start:
        set_exon = set([i for i in range(start_e, end_e+1)])
        cap = set_transcript.intersection(set_exon)
        if len(cap) > 0:            
            transcript_coding_length += len(cap)
            fin_exon_entry.append((exon, min(cap), max(cap)))        
            seq = e_seq[exon]
            if strand == 1:
                fin_exon_coding_seq[exon] = seq[min(cap)-start_e: max(cap) - start_e + 1]
            else:
                fin_exon_coding_seq[exon] = seq[::-1][min(cap)-start_e: max(cap) - start_e + 1][::-1]
        else: pass
    return fin_exon_entry, fin_exon_coding_seq, transcript_coding_length

def find_sconable_site_on_transcript(transcript, n_percent_threshold, split_threshold):
    exon_entry, exon_coding_seq, transcript_coding_length = exon_filter_1(transcript)
    strand = t_strand[transcript]
    coding_size_t = transcript_coding_length       
    ##############################################################################################################################    
    position_threshold = coding_size_t*n_percent_threshold/100    
    exon_size_threshold = 2*split_threshold + 1
    usage_filter = ['', 1] #Consider all
    ##############################################################################################################################    
    profiles = list()
    putative_rank = 0
    cum_size = 0 
    temp_size = 0           
    if strand == 1:
        list_gene_exon = exon_entry
    else:
        list_gene_exon = exon_entry[::-1]
    remained = position_threshold
    for exon, start, end in list_gene_exon: #Coding start and exon. asencing order. if Coding size < 1, discarded.        
        putative_rank += 1          
        coding_size = end - start + 1        
        coding_s, coding_e = start, end
        usage = e_usage[exon]             
        if cum_size < position_threshold: #Filter 1: Coding region start site on first 50%              
            if remained < coding_size:                
                if coding_size > exon_size_threshold:#Filter 2: Exon coding size                 
                    if usage in usage_filter:
                        coding_seq = exon_coding_seq[exon]                           
                        for screening_result in find_sconable_site_on_exon(exon, (coding_s, coding_e), coding_seq):                                                
                            insert, insert_start, insert_end, pam_pos, target_seq, non_pam_seq, fold_sc, target_region = screening_result
                            target_start, target_end = target_region 
                            #print(target_seq, target_region)
                            GC_percent = gccontent(non_pam_seq)             
                            selected = False                   
                            if strand == 1:
                                new_pos_threshold = coding_s + remained                                
                                if insert_start + 2 < new_pos_threshold:
                                    selected = True
                                else: pass
                                left_remain = insert_end - coding_s
                                right_remain = coding_e - insert_end + 1                      
                            else:
                                new_pos_threshold = coding_e - remained                                
                                if insert_start > new_pos_threshold - 1:
                                    selected = True
                                else: pass
                                left_remain = coding_e - insert_end + 3
                                right_remain = insert_start - coding_s + 1                            
                            if left_remain > split_threshold:#Filter 3: Splited site > split_threshold on Left side
                                if right_remain > split_threshold:#Filter 3: Splited site > split_threshold on Right side    
                                    if selected:                                                                                
                                        temp_profile = (exon, target_seq, target_start, target_end, insert, insert_start, insert_end, pam_pos, left_remain, right_remain, GC_percent, putative_rank, usage, fold_sc, cum_size, coding_size_t)
                                        profiles.append(temp_profile) 
                                    else: pass                  
                                else: pass
                            else: pass
                    else: pass
                else: pass
            else:
                if coding_size > exon_size_threshold:#Filter 2: Exon coding size                 
                    if usage in usage_filter:
                        coding_seq = exon_coding_seq[exon]                           
                        for screening_result in find_sconable_site_on_exon(exon, (coding_s, coding_e), coding_seq):                                                
                            insert, insert_start, insert_end, pam_pos, target_seq, non_pam_seq, fold_sc, target_region = screening_result
                            target_start, target_end = target_region
                            #print(target_seq, target_region)
                            GC_percent = gccontent(non_pam_seq)   
                            if strand == 1:               
                                left_remain = insert_end - coding_s
                                right_remain = coding_e - insert_end + 1                      
                            else:
                                left_remain = coding_e - insert_end + 3
                                right_remain = insert_start - coding_s + 1                            
                            if left_remain > split_threshold:#Filter 3: Splited site > split_threshold on Left side
                                if right_remain > split_threshold:#Filter 3: Splited site > split_threshold on Right side          
                                    temp_profile = (exon, target_seq, target_start, target_end, insert, insert_start, insert_end, pam_pos, left_remain, right_remain, GC_percent, putative_rank, usage, fold_sc, cum_size, coding_size_t)
                                    profiles.append(temp_profile)                   
                                else: pass
                            else: pass
                    else: pass
                else: pass
        else: pass
        cum_size += coding_size  
        remained -= coding_size       
    return profiles

############################################################
# 3. Generate Screening Database
############################################################
#In flip, CAGG positioned on external of CRISPR site
n_percent_threshold = 50 #First n% of coding seq
split_threshold = 60 #Size of each splited exon
def mk_output(species_version):
    print(species_version, 'species_version')
    if version == 'vdgn':
        print('This version is vdgn')
    else:
        print('This version is magr')
    Chromosome_blacklist = ['MT', 'mt', 'mitochondrial']
    target_gene = set(gene_canonical_transcript.keys()).intersection(set(g_chromosome.keys()))
    
    # Initialize list to collect output data
    output_data = []
    
    for gene in target_gene:
        target_transcript = gene_canonical_transcript[gene].keys()
        for transcript in target_transcript:
            profiles_res = find_sconable_site_on_transcript(transcript, n_percent_threshold, split_threshold)
            exon_s, exon_e, exon_direction, size, exon_cons, chromosome = None, None, None, None, None, None
            for temp_res in profiles_res:
                exon, target_seq, target_start, target_end, insertion_seq, insert_start, insert_end, pam_pos, left_remain, right_remain, gc_percent, putative_rank, usage_exon, fold_sc, cum_size, coding_size_t = temp_res
                if not exon_s:
                    exon_s, exon_e = e_region[exon]
                    exon_direction = e_strand[exon]
                    size = exon_e - exon_s + 1
                    exon_cons = usage_exon
                    chromosome = str(g_chromosome[gene])
                if chromosome not in Chromosome_blacklist:
                    if exon_direction == 1:
                        output_data.append([gene, chromosome, transcript, exon, putative_rank, exon_cons, exon_s, exon_e, exon_direction, size, insertion_seq, insert_start, insert_end, pam_pos, target_seq, len(target_seq), target_start, target_end, left_remain, right_remain, gc_percent, fold_sc, cum_size, coding_size_t, species_version + '.SCON_DB.parquet'])
                    else:
                        output_data.append([gene, chromosome, transcript, exon, putative_rank, exon_cons, exon_e, exon_s, exon_direction, size, insertion_seq, insert_end, insert_start, pam_pos, target_seq, len(target_seq), target_end, target_start, right_remain, left_remain, gc_percent, fold_sc, cum_size, coding_size_t, species_version + '.SCON_DB.parquet'])
    
    # Check if there is data to save
    if output_data:
        # Create DataFrame and save as Parquet
        column_names = ['Gene', 'Chromosome', 'Transcript', 'Exon', 'Putative_rank', 'Exon_usage', 'Exon_start', 'Exon_end', 'Exon_strand', 'Exon_size', 'Insertion_sequence', 'Insertion_start', 'Insertion_end', 'PAM_position', 'Target_sequence', 'Target_length', 'Tartget_start', 'Tartget_end', 'Left_remain', 'Right_remain', 'GC', 'Self_complement', 'cum_size', 'coding_size_t', 'scon_file']

        df = pd.DataFrame(output_data, columns=column_names)
        # Convert 'Exon_usage' to float, setting errors='coerce' to handle non-numeric values
        df['Exon_usage'] = pd.to_numeric(df['Exon_usage'], errors='coerce')
        df['3N'] = df['Right_remain'].apply(lambda x: 'Y' if x % 3 == 0 else 'N')
        df.to_parquet(f'{species_version}.SCON_DB.parquet', index=False)
        print(f"{species_version}.SCON_DB.parquet saved successfully.")
        print("")
    else:
        print(f"No data to save for {species_version}.")
        print("")
    return

if __name__ == '__main__':
    exon_file = f"{data_dir}/{species_version}.exon_info.fa"
    exon_transcript_file = f"{data_dir}/{species_version}.transcripts_info.csv"
    transcript_file = f"{data_dir}/{species_version}.transcript_utr_seq.fa"
    canonical_transcript_file = f"{data_dir}/{species_version}.appris_data.tsv"
    
    e_seq, e_usage, e_region, e_strand = parse_exon_info(exon_file)
    t_gene, t_e_entry, g_chromosome, g_transcript = parse_exon_transcript_info(exon_transcript_file)
    t_utr, t_strand, t_coding_length = parse_transcript_info(transcript_file)
    gene_canonical_transcript = canonical_transcript_info(canonical_transcript_file, canonical_checking)
    mk_output(species_version)
