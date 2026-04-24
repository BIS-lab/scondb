<script>
    import { Heading, NavLi, NavUl, P } from "flowbite-svelte";
    import { page } from "$app/stores";
    $: activeUrl = $page.url.pathname;
    let activeClass =
        "text-white font-semibold bg-green-700 md:bg-transparent md:text-green-700 md:dark:text-white dark:bg-green-600 md:dark:bg-transparent";
    let nonActiveClass =
        "text-gray-700 hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-green-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent";
</script>

<div class="p-10 w-full min-w-[768px] max-w-[1800px] mx-auto">
    <div class="w-full border-b border-gray-300 mb-8 pb-2">
        <Heading size="2xl" class="text-gray-800 font-bold text-left px-6">
            Tutorial
        </Heading>
    </div>

    <div class="mt-5 p-10 bg-green-50 rounded-lg shadow-sm border border-green-100">
        <P size="lg" weight="normal" class="text-gray-700">
            This page is designed to help you quickly and easily find the information you need. It provides a step-by-step guide on how to use the various features, ensuring an optimal user experience.
        </P>
    </div>

    <div class="my-12 border-t border-gray-200"></div>

    <section class="space-y-10">
        <div class="flex items-center gap-3 flex-nowrap whitespace-nowrap px-2">
            <div class="bg-green-600 text-white px-3 py-1 rounded-full font-bold text-base flex-shrink-0">Step 1</div>
            <Heading tag="h3" class="text-xl font-bold text-gray-800">Select Search Strategy</Heading>
        </div>

        <div class="space-y-6">
            <div class="flex items-center gap-2 px-6">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <P size="lg" weight="bold" class="text-gray-900">Option A: Direct Gene Search</P>
            </div>

            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_1.png" 
                    alt="Direct Search Strategy" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-12 px-6">
                <div class="space-y-4">
                    <P weight="bold" class="text-gray-900 text-lg">1. Select splice junction type:</P>
                    <P class="text-gray-700">
                        These strategies define the specific junction sites where the SCON (189-bp short conditional intron) will be inserted.
                    </P>
                    
                    <ul class="ml-6 space-y-4">
                        <li>
                            <P weight="bold" class="text-gray-900">VDGN (Default)</P>
                            <P size="sm" class="text-gray-600">The SCON is inserted between <span class="font-mono font-bold">VDG | N</span>.</P>
                            <ul class="ml-4 mt-1 text-xs text-gray-500">
                                <li>V: A, C, or G | D: A, G, or T | G: Guanine | N: Any nucleotide</li>
                            </ul>
                        </li>
                        <li>
                            <P weight="bold" class="text-gray-900">MAGR (Stringent)</P>
                            <P size="sm" class="text-gray-600">The SCON is inserted between <span class="font-mono font-bold">MAG | R</span>.</P>
                            <ul class="ml-4 mt-1 text-xs text-gray-500">
                                <li>M: A or C | A: Adenine | G: Guanine | R: A or G</li>
                            </ul>
                        </li>
                    </ul>
                </div>

                <div class="space-y-4">
                    <P weight="bold" class="text-gray-900 text-lg">2. Search Target:</P>
                    <P class="text-gray-700">
                        Input the Species name (e.g., <em class="text-gray-800">Mus musculus</em>) and enter the official Gene Symbol (e.g., <em class="text-gray-800">Alb, Sox2</em>).
                    </P>
                    <div class="p-4 bg-gray-50 border-l-4 border-green-500 rounded-r-md">
                        <P size="sm" class="text-gray-600 italic">
                            Tip: Use the auto-complete suggestions to ensure correct genomic data assembly is loaded.
                        </P>
                    </div>
                </div>
            </div>
        </div>

        <div class="my-8 border-t border-dashed border-gray-200"></div>

        <div class="space-y-6">
            <div class="flex items-center gap-2 px-6">
                <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                <P size="lg" weight="bold" class="text-gray-900">Option B: Browse Dataset</P>
            </div>

            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_2.png" 
                    alt="Browse Dataset Strategy" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>

            <div class="px-10 w-full">
                <div class="flex items-start gap-4">
                    <P weight="bold" class="text-green-600 text-xl">•</P>
                    <div class="space-y-3">
                        <P weight="bold" class="text-gray-900 text-lg">Browse Dataset:</P>
                        <P class="text-gray-700 leading-relaxed">
                            Alternatively, navigate to the <span class="font-bold text-green-700">Dataset</span> menu to filter by Species and Ensembl release version. 
                            Clicking <span class="px-2 py-0.5 bg-gray-100 border border-gray-300 rounded text-sm font-bold text-gray-800">Go to Analysis</span> on your preferred version 
                            will directly take you to the "Analysis" session with the pre-selected parameters.
                        </P>
                    </div>
                </div>
            </div>
        </div>
    </section>
<div class="my-16 border-t border-gray-200"></div>

    <section class="space-y-10 pb-20">
        <div class="flex items-center gap-3 flex-nowrap whitespace-nowrap px-2">
            <div class="bg-green-600 text-white px-3 py-1 rounded-full font-bold text-base flex-shrink-0">Step 2</div>
            <Heading tag="h3" class="text-xl font-bold text-gray-800">Identify candidate sites</Heading>
        </div>

        <div class="space-y-6">
            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_3.png" 
                    alt="SCON Targetable Sites and Exon Info Preview" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>

            <div class="px-10 w-full space-y-8">
                <div class="flex items-start gap-4">
                    <P weight="bold" class="text-green-600 text-xl">•</P>
                    <div class="space-y-3">
                        <P weight="bold" class="text-gray-900 text-lg">SCON Targetable Sites Table:</P>
                        <P class="text-gray-700 leading-relaxed">
                            This table serves as a map for your target gene. It lists every known transcript and identifies which exons can be modified using the SCON system. 
                            Click on a <span class="font-bold text-green-700">specific number</span> in the transcript columns to load the detailed sequence and gRNA design options. 
                            You can also click on any <span class="font-semibold text-gray-900 underline">Transcript ID</span> in the table header to be redirected to the Ensembl website for in-depth information.
                        </P>
                    </div>
                </div>
            </div>

            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_4.png" 
                    alt="Exon Info Preview" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>
            <div class="px-10 w-full space-y-8">

                <div class="flex items-start gap-4">
                    <P weight="bold" class="text-green-600 text-xl">•</P>
                    <div class="space-y-3">
                        <P weight="bold" class="text-gray-900 text-lg">Exon Info Overview:</P>
                        <P class="text-gray-700 leading-relaxed">
                            Once a specific exon-transcript combination is selected, the Exon Info table provides a comprehensive profile of the target exon's genomic properties. 
                            The <span class="font-bold text-gray-900">Exon Usage</span> score indicates whether the exon is consistently included across all transcripts for that gene. 
                            We highly recommend prioritizing exons with a <span class="text-green-700 font-bold text-lg">score of 1</span>, as these are constitutive exons ensuring a more robust knockout effect across all protein variants.
                        </P>
                    </div>
                </div>

                <div class="ml-8 space-y-4">
                    <P weight="bold" class="text-gray-800 text-base">Column Descriptions:</P>
                    <ul class="space-y-3 text-gray-700">
                        <li class="flex items-baseline gap-2">
                            <span class="text-green-600 text-xs">■</span>
                            <P size="sm"><span class="font-bold text-gray-900">Gene / Transcript / Exon:</span> Identifies the specific genomic features currently under analysis.</P>
                        </li>
                        <li class="flex items-baseline gap-2">
                            <span class="text-green-600 text-xs">■</span>
                            <P size="sm"><span class="font-bold text-gray-900">Exon Usage:</span> Binary indicator (0 or 1) of exon presence across all isoforms.</P>
                        </li>
                        <li class="flex items-baseline gap-2">
                            <span class="text-green-600 text-xs">■</span>
                            <P size="sm"><span class="font-bold text-gray-900">Exon Size / Strand:</span> Length of the target exon in bp and its orientation (1 or -1) on the chromosome.</P>
                        </li>
                        <li class="flex items-baseline gap-2">
                            <span class="text-green-600 text-xs">■</span>
                            <P size="sm"><span class="font-bold text-gray-900">Chromosome / Exon Start / End:</span> Precise chromosomal coordinates of the selected exon.</P>
                        </li>
                        <li class="flex items-baseline gap-2">
                            <span class="text-green-600 text-xs">■</span>
                            <P size="sm"><span class="font-bold text-gray-900">Cumulative CDS Size / Total Coding Size:</span> Length of the coding sequence up to the current exon and for the entire transcript, useful for mapping functional protein domains.</P>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
<div class="my-16 border-t border-gray-200"></div>

    <section class="space-y-10 pb-32">
        <div class="flex items-center gap-3 flex-nowrap whitespace-nowrap px-2">
            <div class="bg-green-600 text-white px-3 py-1 rounded-full font-bold text-base flex-shrink-0">Step 3</div>
            <Heading tag="h3" class="text-xl font-bold text-gray-800">Evaluate and Select gRNAs</Heading>
        </div>

        <div class="space-y-6">
            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_5.png" 
                    alt="Sequence Browser and Detailed Site Analysis" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>

            <div class="px-10 w-full space-y-10">
                <div class="flex items-start gap-4">
                    <P weight="bold" class="text-green-600 text-xl">•</P>
                    <div class="space-y-3">
                        <P weight="bold" class="text-gray-900 text-lg">Sequence Browser:</P>
                        <P class="text-gray-700 leading-relaxed">
                            The Sequence Browser provides a high-resolution visualization of the SCON insertion site. 
                            <span class="font-bold text-gray-900">Black bars</span> represent the SCON target site (MAGR or VDGN), while <span class="font-bold text-emerald-500">Emerald highlights</span> indicate the PAM (Protospacer Adjacent Motif) sequences. 
                            This allows you to visually verify the spatial relationship between the CRISPR cut site and the intended intron insertion point.
                        </P>
                    </div>
                </div>
            </div>
            <div class="flex justify-center py-4">
                <img 
                    src="/genpos_tutorial_6.png" 
                    alt="Detailed Site Analysis" 
                    class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
                />
            </div>

            <div class="px-10 w-full space-y-10">
                <div class="flex items-start gap-4">
                <P weight="bold" class="text-green-600 text-xl">•</P>
                    <div class="space-y-3">
                        <P weight="bold" class="text-gray-900 text-lg">Detailed Site Analysis:</P>
                        <P class="text-gray-700 leading-relaxed">
                            Below the browser, you will find a summary table where each row corresponds to the target bars (black/emerald) shown in the sequence. Click the <span class="font-bold text-gray-900">downward chevron</span> on the left side of a row to expand the detailed sub-table. This provides comprehensive data for each gRNA candidate, offering direct assistance in selecting the most reliable targetable site. To assist your selection, we provide a <span class="font-bold text-green-700">Combined Score</span> that weights parameters such as MM_score, GC content, Distance from cut, and the In-frame compatibility. While a higher score generally indicates a better-optimized design, you should evaluate each parameter based on your specific experimental goals.
                        </P>
                    </div>
                </div>

            <div class="p-4 bg-gray-50 border-l-4 border-yellow-400 rounded-r-md">
                <P size="sm" class="text-gray-700">
                    <span class="font-bold text-gray-900">[Caution!]</span> We offer candidate information as a reference, but please note that the <span class="font-bold text-gray-900">Combined Score</span> results have not been experimentally verified. You can customize the filters depending on your priorities and interests.
                </P>
            </div>

            <div class="ml-8 space-y-4">
                <P weight="bold" class="text-gray-800 text-base">Column Descriptions:</P>
                <ul class="space-y-4 text-gray-700">
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Insertion_sequence:</span> The specific genomic sequence at the junction where the SCON is inserted. This is used to design the homology arms for your donor template (ssODN).</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Insertion_start / End:</span> The exact chromosomal coordinates where the SCON will be inserted into the genome.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Left_remain / Right_remain:</span> The length of the remaining exon sequences on the left and right sides of the SCON insertion site. These values are critical for ensuring the structural integrity of the flanking exons.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">n_editable:</span> The total number of unique sgRNAs available to target this specific insertion site.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">PAM_position:</span> The Protospacer Adjacent Motif (NGG) and its location (Left or Right) relative to the target sequence.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Target Sequence:</span> The 20bp guide RNA (sgRNA) sequence.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Target_start / End:</span> The chromosomal coordinates where the gRNA actually targets and cuts the DNA.</P>
                    </li>
                    
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <div class="space-y-1">
                            <P size="sm"><span class="font-bold text-gray-900">Combined Score:</span> An integrated ranking metric that evaluates gRNA performance by balancing multiple critical factors.</P>
                            <P size="xs" class="text-gray-500 ml-2">
                                It computationally weights <span class="font-semibold text-gray-700">Specificity</span> (minimizing off-targets via MM_score, max 30), <span class="font-semibold text-gray-700">Efficiency</span> (optimal GC content, max 30 and low self-complementarity, max 10), and <span class="font-semibold text-gray-700">Knock-in Precision</span> (prioritizing shorter distance from cut, max 20). This score helps you identify candidates that maximize successful SCON insertion while ensuring an effective gene knockout even if alternative splicing occurs. (In-frame status, max 10).
                            </P>
                        </div>
                    </li>

                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">GC Content (%):</span> The percentage of G and C nucleotides in the sgRNA. The optimal range for efficiency is 40% – 60%.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Self_complement:</span> A score predicting the likelihood of the sgRNA forming internal hairpin structures. Lower scores suggest better activity.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">MM_score (MM0, MM1, MM2):</span> The number of genomic sites with 0, 1, or 2 mismatches. Lower counts (ideally 1, 0, 0) indicate high specificity.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">Distance from cut:</span> The distance (bp) between the CRISPR cut site and the SCON insertion point. Note: Shorter distances typically lead to higher knock-in efficiency.</P>
                    </li>
                    <li class="flex items-baseline gap-2">
                        <span class="text-green-600 text-xs">■</span>
                        <P size="sm"><span class="font-bold text-gray-900">In_frame (3N):</span> Indicates whether the insertion length maintains the triplet codon frame, helping predict functional stability during alternative splicing.</P>
                    </li>
                </ul>
            </div>
        </div>
    </section>

    <div class="my-16 border-t border-gray-200"></div>

    <section class="space-y-10 pb-32">
        <div class="flex items-center gap-3 flex-nowrap whitespace-nowrap px-2">
            <div class="bg-green-600 text-white px-3 py-1 rounded-full font-bold text-base flex-shrink-0">Step 4</div>
            <Heading tag="h3" class="text-xl font-bold text-gray-800">Export Experimental Design</Heading>
        </div>

        <div class="flex justify-center py-4">
            <img 
                src="/genpos_tutorial_7.png" 
                alt="Export Experimental Design" 
                class="w-full max-w-5xl rounded-xl shadow-lg border border-gray-200"
            />
        </div>

        <div class="px-10 w-full space-y-10">
            <div class="flex items-start gap-4">
                <P weight="bold" class="text-green-600 text-xl">•</P>
                <div class="space-y-3">
                    <P weight="bold" class="text-gray-900 text-lg">Download ssODN:</P>
                    <P class="text-gray-700 leading-relaxed">
                        Once you’ve selected the optimal site, click the <span class="font-bold text-green-600">🧬 Download ssODN</span> button to get the final donor sequence (Left arm + SCON + Right arm) for your knock-in experiment.
                    </P>
                </div>
            </div>

            <div class="flex items-start gap-4">
                <P weight="bold" class="text-green-600 text-xl">•</P>
                <div class="space-y-3">
                    <P weight="bold" class="text-gray-900 text-lg">Full Report:</P>
                    <P class="text-gray-700 leading-relaxed">
                        Use the <span class="font-bold text-green-700">⬇ Download Table</span> button to save all candidate data for your records.
                    </P>
                </div>
            </div>
        </div>
    </section>
</div>
