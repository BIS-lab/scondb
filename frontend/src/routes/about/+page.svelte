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
    <div class="w-full border-b border-gray-300 mb-4 pb-2">
        <Heading size="2xl" class="text-gray-800 font-bold text-left px-6">
          About SCON
        </Heading>
      </div>

    <div class="mt-5 p-10 bg-green-50 rounded-lg">
        <P size="medium" weight="normal"
            ><strong>SCON (Short Conditional intrON)</strong> is a next-generation genetic tool designed to radically simplify functional studies across 300+ vertebrate species. With a compact length of only <strong>189 bp</strong>, SCON enables the rapid generation of conditional knockout alleles through a streamlined, one-step process.
        </P>
    </div>
    <div class="my-16 border-t border-gray-200"></div>

    <section class="grid grid-cols-1 xl:grid-cols-2 gap-12 px-6 items-start">
        <div class="flex justify-center">
            <img 
                src="/about_scon_1.png" 
                alt="SCON Mechanism Diagram" 
                class="w-full max-w-2xl rounded-xl shadow-sm border border-gray-100"
            />
        </div>

        <div class="space-y-8">
            <div class="space-y-4">
                <Heading tag="h3" class="text-2xl font-bold text-gray-800 border-l-4 border-green-600 pl-4">What is SCON?</Heading>
                <P size="lg" class="text-gray-700 leading-relaxed">
                    <span class="font-bold text-green-700">SCON</span> is a high-performance, 189-bp artificial intron engineered for the rapid generation of conditional knockout (cKO) models across multiple species. Originally derived from the human HBB (Hemoglobin subunit beta) gene, SCON has been optimized to serve as a "genetic switch" that can be integrated into a single exon using CRISPR/Cas9-mediated knock-in.
                </P>
            </div>

            <div class="space-y-6">
                <Heading tag="h4" class="text-xl font-bold text-gray-800">Mechanism of Action</Heading>
                <div class="space-y-4">
                    <div>
                        <P weight="bold" class="text-gray-900">1. Default "ON" State:</P>
                        <P class="text-gray-600 ml-4 mt-1">
                            Upon insertion into a coding exon, SCON is recognized by the cellular spliceosome as a standard intron. It is precisely spliced out during mRNA processing, leaving the protein-coding sequence intact and maintaining wild-type expression levels.
                        </P>
                    </div>

                    <div>
                        <P weight="bold" class="text-gray-900">2. Conditional "OFF" State (Knockout):</P>
                        <P class="text-gray-600 ml-4 mt-1">
                            The SCON sequence contains recombination sites (e.g., LoxP or FRT) flanking its critical splicing elements. When exposed to Cre or Flp recombinase, the SCON sequence is inverted or its splicing signals are disrupted. This leads to:
                        </P>
                        <ul class="ml-10 mt-2 space-y-2 text-gray-600 list-disc">
                            <li><P size="sm">Intron Retention/Mis-splicing: The SCON sequence is no longer spliced out.</P></li>
                            <li><P size="sm">Premature Termination: The retained sequence introduces multiple stop codons and triggers a frame-shift, resulting in complete loss of gene function.</P></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div class="my-16 border-t border-gray-200"></div>

    <section class="space-y-8 px-6">
        <Heading tag="h3" class="text-2xl font-bold text-gray-800 border-l-4 border-green-600 pl-4">Key Advantages for Researchers</Heading>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="space-y-2">
                <P weight="bold" class="text-gray-900">One-Step Zygote Injection</P>
                <P size="sm" class="text-gray-600">Due to its compact size (189 bp), SCON can be delivered via ssODN (single-stranded DNA) donors through a single injection, bypassing the need for complex and time-consuming ES cell targeting.</P>
            </div>
            <div class="space-y-2">
                <P weight="bold" class="text-gray-900">Universal Applicability</P>
                <P size="sm" class="text-gray-600">As demonstrated in the latest research, SCON's functionality is highly conserved across vertebrates, including mice, human iPSCs, zebrafish, Xenopus, and various species.</P>
            </div>
            <div class="space-y-2">
                <P weight="bold" class="text-gray-900">Minimal Hypomorphic Risk</P>
                <P size="sm" class="text-gray-600">Unlike traditional "floxing," SCON is placed within a single exon, minimizing the risk of reduced gene expression in the "ON" state.</P>
            </div>
        </div>
    </section>

    <div class="my-16 border-t border-gray-200"></div>

    <section class="grid grid-cols-1 xl:grid-cols-2 gap-12 px-6 items-center pb-20">
        <div class="space-y-10">
            <div class="space-y-4">
                <Heading tag="h3" class="text-2xl font-bold text-gray-800 border-l-4 border-green-600 pl-4">Database Construction & Filtering</Heading>
                <P class="text-gray-600 pl-4">To ensure high-precision targeting and robust conditional knockout performance, our database was constructed using a systematic filtering pipeline.</P>
            </div>

            <div class="space-y-6">
                <P weight="bold" class="text-gray-900 text-lg">1. Filtering Targetable Exons</P>
                <P class="text-gray-700 ml-4">The pipeline begins by identifying exons that are suitable for SCON insertion based on their structural and functional properties:</P>
                <ul class="ml-10 space-y-4">
                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700">
                            <span class="font-bold">CDS Location:</span> Only exons located within the <span class="font-semibold text-gray-900">first 50%</span> of the coding sequence (CDS) are selected to ensure that any induced truncation results in a complete loss-of-function.
                        </P>
                    </li>

                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700">
                            <span class="font-bold">Split Exon Balance:</span> To maintain splice donor(SD) and splice acceptor(SA) stability, the insertion site must leave at least <span class="font-semibold text-gray-900">60 bp</span> of exon sequence on both the 5' and 3' sides of the SCON (Left_remain & Right_remain >= 60 bp).
                        </P>
                    </li>
                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700">
                            <span class="font-bold">Exon Length:</span> A minimum length of <span class="font-semibold text-gray-900">120 bp</span> is required for the target exon.
                        </P>
                    </li>
                </ul>

                <P weight="bold" class="text-gray-900 text-lg">2. Choose Splice Junction Motif</P>
                <P class="text-gray-700 ml-4">Following the optimized splicing consensus, sites are chosen by their flanking 4-nucleotide motifs:</P>
                <ul class="ml-10 space-y-3">
                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700"><span class="font-bold">MAGR (Stringent):</span> Targets <span class="font-mono font-bold">(A/C)AG | (A/G)</span> sites. This represents the most conserved mammalian splice junction for maximum splicing efficiency.</P>
                    </li>
                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700"><span class="font-bold">VDGN (Flexible):</span> Targets <span class="font-mono font-bold">(A/G/C)(A/T/G)G | (A/T/G/C)</span> sites, allowing for broader genomic coverage.</P>
                    </li>
                    <li class="flex items-start gap-2">
                        <span class="text-green-600 font-bold">•</span>
                        <P class="text-gray-700"><span class="font-bold">Insertion Site:</span> The SCON is precisely inserted between the <span class="font-bold">3rd and 4th nucleotides</span> of the identified motif.</P>
                    </li>
                </ul>
            </div>
        </div>

        <div class="flex justify-center">
            <img 
                src="/scondb_overview2.svg" 
                alt="Database Filtering Pipeline Diagram" 
                class="w-full max-w-2xl rounded-xl shadow-md border border-gray-100"
            />
        </div>
    </section>
</div>
