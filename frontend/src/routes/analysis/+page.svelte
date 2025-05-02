<script>
    import {
        Heading,
        P,
        A,
        Spinner,
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Radio,
        Checkbox,
        Popover,
        Button,
    } from "flowbite-svelte";
    import { selectedSpecies, push, selectedtype } from "../../lib/stores";
    import { load } from "../../lib/fetch";
    import { debounce } from "../../lib/utils";
    import { onMount, onDestroy } from "svelte";
    import { SearchOutline, ChevronDownOutline } from "flowbite-svelte-icons";
    let species = "";
    let selected = "";
    let isLoading = false;
    let sconable;
    let sconable_columns;
    let exoninfo;
    let cexoninfo;
    let maxVal = null;
    let clickedRows = [];
    let sequence;
    let chunkedSeq;
    let selectedRadio;
    let lastSelected = "";
    let cachedSpeciesData = {};
    let isLoadingSequence = false;
    let isLoadingSconable = false;


    function toggleClick(index) {
        clickedRows[index] = !clickedRows[index];
        console.log("clickedRows", clickedRows);
    }

    let suggestions = [];
    let allSpecies = [];
    let selectSuggestions = [];
    let selectOptions = [];

    const debouncedFetchData = debounce(fetchData, 300);

    push.subscribe((value) => {
        console.log(value, "push_value");
        if (value) {
            selectedSpecies.subscribe((value) => {
                species = value;
            });
            selectedtype.subscribe((value) => {
                selectedRadio = value;
            });
            debouncedFetchData();
        } else {
            selectedSpecies.set(null);
        }
    });

    async function load_data(selectedRadio) {
        const metaData = await load(`meta/dataset?type=${selectedRadio}`);
        //console.log(" metaData loaded:", metaData);
        const filtered = metaData.filter(e => {
            if (e.species === "mus_musculus") {
                return e.ensemble_rev === 109;
            }
            return true;
        });

        allSpecies = [...new Set(filtered.map(e => e.species))];
    }

    async function fetchData() {
        isLoading = true;
        if (species && !cachedSpeciesData[species]) {
            console.log("Fetching data for species:", species);
            const speciesData = await load(
                `sconable_genes?species=${species}&ensemble_rev=109&type=${selectedRadio}`,
            );
            cachedSpeciesData[species] = speciesData.map((e) => e.name);
        }
        console.log(cachedSpeciesData[species], species, "ggggggggg");
        selectOptions = cachedSpeciesData[species] || [];
        //selectSuggestions = selectOptions;
        isLoading = false;
    }

    

    function handleInput(event) {
        species = event.target.value;
        updateSuggestions();
    }

    const debouncedUpdateSelectSuggestions = debounce(
        updateSelectSuggestions,
        500,
    );

    function handleSelectInput(event) {
        const newSelected = event.target.value;
        if (newSelected !== lastSelected) {
            selected = newSelected;
            debouncedUpdateSelectSuggestions();
            lastSelected = newSelected;
        }
    }

    function updateSuggestions() {
        if (species) {
            suggestions = allSpecies.filter((item) =>
                item.toLowerCase().includes(species.toLowerCase()),
            );
        } else {
            suggestions = [];
        }
    }

    function updateSelectSuggestions() {
        if (selected) {
            const lowerSelected = selected.toLowerCase();
            selectSuggestions = selectOptions.filter((item) =>
                item.toLowerCase().includes(lowerSelected),
            );
        } else {
            selectSuggestions = [];
        }
        //console.log(selectSuggestions, "gggggg");
    }

    function handleSuggestionClick(suggestion) {
        species = suggestion;
        selectedSpecies.update(() => suggestion);
        selected = "";
        suggestions = [];
        debouncedFetchData();
    }

    function handleSelectSuggestionClick(select) {
        selected = select;
        selectSuggestions = [];
    }

    async function Search_SCONablesite(species, selected) {
        isLoadingSconable = true;
        sconable = null;
        exoninfo = null;

        sconable = await load(
            `sconable_site_count_by_transcript?species=${species}&ensemble_rev=109&gene=${selected}&type=${selectedRadio}`,
        );
        exoninfo = await load(
            `sconable_sites_group?species=${species}&ensemble_rev=109&gene=${selected}&type=${selectedRadio}`,
        );

        sconable.rows.forEach((item) => {
            Object.values(item).forEach((value) => {
                if (typeof value === "number" && (maxVal === null || value > maxVal)) {
                    maxVal = value;
                }
            });
        });
        sconable_columns = Object.keys(sconable.rows[0]);
        isLoadingSconable = false;
    }

    function chunkArray(array, chunkSize) {
        const results = [];
        for (let i = 0; i < array.length; i += chunkSize) {
            results.push(array.slice(i, i + chunkSize));
        }
        return results;
    }
    let pamHighlights = [];

    async function Search_ExonInfo(cexon, ctranscript) {
        isLoadingSequence = true;
        cexoninfo = exoninfo.filter((v) => v.Exon === cexon && v.Transcript === ctranscript);
        const strand = Number(cexoninfo[0]?.Exon_strand) || 1;

        clickedRows = new Array(maxVal).fill(false);
        clickedRows[0] = true;

        sequence = await load(
            `scon_sites_by_transcript?species=${species}&ensemble_rev=109&exon=${cexon}&transcript=${ctranscript}&type=${selectedRadio}`,
        );
        pamHighlights = cexoninfo.flatMap((c) =>
            c.scon_sites.map((s) => {
                const start = Number(s.Tartget_start);
                const end = Number(s.Tartget_end);
                const PAM = s.PAM_position;
                return { pos: (PAM === "right" ? end : start) };
            }),
        );
        chunkedSeq = chunkArray(sequence, 10);
        isLoadingSequence = false;
    }

    let hoveredRow = null;
    let hoveredPAM = null;

    function handleRowMouseEnter(index, start, end, scon_sites) {
        if (start > end) {
        [start, end] = [end, start];
        }

        hoveredRow = { index, start, end };

        hoveredPAM = scon_sites.map((c) => {
            let s = Number(c.Tartget_start);
            let e = Number(c.Tartget_end);
            if (s > e) [s, e] = [e, s];
            return {
                target_start: s,
                target_end: e,
                PAM_position: c.PAM_position,
                strand: Number(cexoninfo[0]?.Exon_strand) || 1,
            };
        });

        console.log(hoveredPAM, "hoveredPAM");
    }

    function handleRowMouseLeave() {
        hoveredRow = null;
        hoveredPAM = null;
    }

    function highlightFromBox(start, end) {
        if (start > end) [start, end] = [end, start];
        hoveredRow = { index: -1, start, end };
        hoveredPAM = null;
    }

    function isPAMPosition(pos, PAM) {
        if (!PAM) return false;
        return PAM.some((site) =>
            site.target_start <= site.target_end
                ? pos >= Number(site.target_start) && pos <= Number(site.target_end)
                : pos >= Number(site.target_end) && pos <= Number(site.target_start),
        );
    }

    function getClassForBackground(s, hoveredRow, hoveredPAM) {
        if (!hoveredRow) return "";

        const inHighlight =
            hoveredRow.start <= hoveredRow.end
                ? s.pos >= hoveredRow.start && s.pos <= hoveredRow.end
                : s.pos >= hoveredRow.end && s.pos <= hoveredRow.start;

        const isHighlighted = inHighlight;
        const isTarget = isPAMPosition(s.pos, hoveredPAM);

        if (isHighlighted) return "bg-yellow-100";
        if (isTarget) return "bg-green-200";
        return "";
    }

    function handleRadioChange(value) {
        selectedRadio = value;
        species = "";
        selected = "";
    }

    function isPAMLetter(pos) {
        return pamHighlights.some(p => p.pos === pos);
    }

    function escapeCSV(value) {
        if (typeof value === "string" && value.includes(",")) {
            return `"${value.replace(/"/g, '""')}"`; 
        }
        return value;
    }

    function downloadAllCSV() {
        if (!cexoninfo || cexoninfo.length === 0) return;

        const headers = [
            "Exon", "Transcript", "Insertion_sequence", "Insertion_start",
            "Insertion_end", "Left_remain", "Right_remain", "Self_complement",
            "n_editable", "PAM_position", "Target_sequence", "Target_length",
            "Target_start", "Target_end", "GC", "MM_score", "In_frame"
        ];

        const rows = cexoninfo.flatMap(c =>
            c.scon_sites.map(site => [
                c.Exon,
                c.Transcript,
                c.Insertion_sequence,
                c.Insertion_start,
                c.Insertion_end,
                c.Left_remain,
                c.Right_remain,
                c.Self_complement,
                c.n_editable,
                site.PAM_position,
                site.Target_sequence,
                site.Target_length,
                site.Tartget_start,
                site.Tartget_end,
                site.GC,
                site.MM_score,
                site["3N"] ?? ""
            ])
        );

        const csvContent = [
            headers.join(","),
            ...rows.map(row => row.map(escapeCSV).join(","))
        ].join("\n");

        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `sconable_sites_${species}_${selected}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }


    function downloadHomologyArmsSingle(c) {
        if (!sequence || !c) return;

        const strand = Number(c.Exon_strand || 1);
        const insSeq = c.Insertion_sequence;
        const insStart = Number(c.Insertion_start);
        const insEnd = Number(c.Insertion_end);
        const cutSite = strand === 1 ? insStart : insEnd;

        const leftFlankLen = 57;
        const rightFlankLen = 59;
        const left3 = insSeq.slice(0, 3);
        const right1 = insSeq.slice(-1);

        let leftFlank, rightFlank, left_arm, right_arm;

        if (strand === 1) {
            const leftStart = cutSite - leftFlankLen;
            const leftEnd = cutSite;
            const rightStart = insEnd + 1;
            const rightEnd = insEnd + rightFlankLen + 1;

            leftFlank = sequence.filter(s => s.pos >= leftStart && s.pos < leftEnd).map(s => s.base).join("");
            rightFlank = sequence.filter(s => s.pos >= rightStart && s.pos < rightEnd).map(s => s.base).join("");

            left_arm = leftFlank + left3;
            right_arm = right1 + rightFlank;
        } else {
            const leftStart = insStart - 5 - leftFlankLen;
            const leftEnd = insStart - 3;
            const rightStart = cutSite + 4;
            const rightEnd = cutSite + 2 + rightFlankLen;

            leftFlank = sequence.filter(s => s.pos >= leftStart && s.pos < leftEnd).map(s => s.base).join("");
            rightFlank = sequence.filter(s => s.pos >= rightStart && s.pos < rightEnd).map(s => s.base).join("");

            leftFlank = reverseSeq(leftFlank);
            rightFlank = reverseSeq(rightFlank);

            left_arm = rightFlank + left3;
            right_arm = right1 + leftFlank;
        }
        const direction = strand === -1 ? "reverse" : "forward";
        const header = `>Exon_${c.Exon}_Transcript_${c.Transcript}_Insertion_${insSeq}_${c.Insertion_start}-${c.Insertion_end}_${direction}`;
        const SCON = "GTAAGTAATAACTTCGTATAAGGTATCCTATACGAAGTTATTCTCTCTGCCTATTGGGGTTACAAGACAGGTTTAAGGAGACCAATAGAAACTGGGCATGTGGAGACAGAGAAGACTCTTGGGTTTCTGATAGGCACTGACATAACTTCGTATAAGGTATCCTATACGAAGTTATTTTCCCTCCCTCAG";
        const sequenceLine = left_arm + SCON + right_arm;

        const content = `${header}\n${sequenceLine}`;
        const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `ssODN_${species}_${selected}.txt`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function reverseSeq(seq) {
        const comp = { A: "T", T: "A", C: "G", G: "C", N: "N" };
        return seq.split("").reverse().map(b => comp[b] || b).join("");
    }


    $: {
        if (selectedRadio) {
            load_data(selectedRadio);
        }
    }
    onMount(() => {
        if (!selectedRadio) {
            selectedRadio = "MAGR";
        }
        load_data(selectedRadio);
        if (!species) {
            species = "";
            selected = "";
        }
    });
    $: chevronTrack = sequence
    ? (Number(cexoninfo[0]?.Exon_strand) === 1
        ? ">".repeat(sequence.length)
        : "<".repeat(sequence.length))
    : "";


//This is for the stacking black line in scroll.
    let targetBoxes = [];

    function calculateTargetLayers(targets) {
        const layers = [];

        targets.forEach((box) => {
            let placed = false;

            for (let layer of layers) {
                const overlap = layer.some((b) => !(box.end < b.start || box.start > b.end));
                if (!overlap) {
                    layer.push(box); 
                    placed = true;
                    break;
                }
            }

            if (!placed) {
                layers.push([box]); 
            }
        });

        return layers.flatMap((layer, i) =>
            layer.map((b) => ({ ...b, topOffset: -0.5 - i * 0.5 })) 
        );
    }

    $: if (sequence && cexoninfo) {
        const strand = Number(cexoninfo[0]?.Exon_strand) || 1;

        const rawTargets = cexoninfo.flatMap((c) =>
            c.scon_sites.map((s) => {
                let sPos = Number(s.Tartget_start);
                let ePos = Number(s.Tartget_end);
                if (sPos > ePos) [sPos, ePos] = [ePos, sPos];

                const rawPam = s.PAM_position;
                const correctedPam =
                    strand === -1
                        ? rawPam === "right"
                            ? "left"
                            : "right"
                        : rawPam;

                return {
                    start: sPos,
                    end: ePos,
                    pam: correctedPam,
                };
            })
        );

        targetBoxes = calculateTargetLayers(rawTargets);
    }
    
</script>

<div class="p-10 w-full">
    <div class="w-full border-b border-gray-300 mb-4 pb-2">
        <Heading size="2xl" class="text-gray-800 font-bold text-left px-6">
          SCON targetable site
        </Heading>
      </div>
    <div class="p-3 z-100">
        <P size="xl" weight="semibold">Search</P>
        <div class="p-3">
            <Radio
                name="radio"
                color="green"
                bind:group={selectedRadio}
                value="MAGR"
                on:change={() => handleRadioChange("MAGR")}
            >
                MAGR
            </Radio>
            <Radio
                name="radio"
                color="green"
                bind:group={selectedRadio}
                value="VDGN"
                on:change={() => handleRadioChange("VDGN")}
            >
                VDGN
            </Radio>
        </div>
        <form class="flex">
            <div class="relative">
                <input
                    type="text"
                    id="species_input"
                    bind:value={species}
                    required
                    placeholder="Search Species"
                    on:input={handleInput}
                    class="h-10 rounded-lg rounded-e-none block disabled:cursor-not-allowed disabled:opacity-50 rtl:text-right p-2.5 focus:border-green-400 focus:ring-green-400 dark:focus:border-green-400 dark:focus:ring-green-400 bg-green-500 text-white dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 text-sm suggestion-list placeholder-white"
                />
                {#if suggestions.length > 0}
                    <ul
                        class="absolute suggestion-list bg-white border border-gray-300 mt-2 rounded-lg shadow-lg flex flex-col z-10"
                    >
                        {#each suggestions as suggestion}
                            <button
                                class="p-2 cursor-pointer hover:bg-gray-100"
                                on:click={() =>
                                    handleSuggestionClick(suggestion)}
                            >
                                {suggestion}
                            </button>
                        {/each}
                    </ul>
                {/if}
            </div>

            <div class="relative">
                <input
                    type="text"
                    id="select_input"
                    bind:value={selected}
                    required
                    placeholder="Search Gene"
                    on:input={handleSelectInput}
                    class="h-10 block border-l-0 disabled:cursor-not-allowed disabled:opacity-50 rtl:text-right p-2.5 focus:border-green-400 focus:ring-green-400 dark:focus:border-green-400 dark:focus:ring-green-400 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 dark:border-gray-600 text-sm suggestions-list"
                />
                {#if isLoading}
                    <Spinner
                        class="absolute right-0 top-0 m-2"
                        color="green"
                        size={6}
                    />
                {/if}{#if !isLoading && selectSuggestions.length > 0}
                    <ul
                        class="absolute suggestions-list bg-white border border-gray-300 mt-2 rounded-lg shadow-lg flex flex-col z-10"
                    >
                        {#each selectSuggestions as suggestion}
                            <button
                                class="p-2 cursor-pointer hover:bg-gray-100 z-10"
                                on:click={() =>
                                    handleSelectSuggestionClick(suggestion)}
                            >
                                {suggestion}
                            </button>
                        {/each}
                    </ul>{/if}
            </div>
            <div>
                <button
                    on:click={() => Search_SCONablesite(species, selected)}
                    color="green"
                    class="h-10 rounded-s-none text-center font-medium focus-within:outline-none inline-flex items-center justify-center px-5 py-2.5 text-sm text-white bg-green-500 hover:bg-green-800 dark:bg-green-600 dark:hover:bg-green-700 rounded-lg h-10 rounded-s-none"
                >
                    <SearchOutline />
                </button>
            </div>
        </form>
    </div>
    <div class="p-3">
        <div class="flex items-center gap-2">
            <P size="xl" weight="semibold" class="py-3">SCON targetable sites</P>
            {#if isLoadingSconable}
                <Spinner size="6" color="green" />
            {/if}
        </div>
        {#if sconable}
            <Table class="overflow-x-scroll w-full outer-table">
                <TableHead>
                    {#each sconable.columns as s, i}
                        {#if s === "Exon"}
                            <TableHeadCell>{s}/Transcript</TableHeadCell>
                        {:else}
                            <TableHeadCell>
                                <A
                                    href={`https://asia.ensembl.org/${species}/Transcript/Summary?t=${s}`}
                                    target="_blank"
                                    class="underline hover:no-underline">{s}</A
                                >
                            </TableHeadCell>
                        {/if}
                    {/each}
                </TableHead>
                <TableBody tableBodyClass="divide-y">
                    {#each sconable.rows as k, i}
                        <TableBodyRow>
                            {#each sconable.columns as c, j}
                                {#if k[c] === null}
                                    <TableBodyCell>0</TableBodyCell>
                                {:else if c !== "Exon"}
                                    <th
                                        on:click={() =>
                                            Search_ExonInfo(k.Exon, c)}
                                        class="px-6 py-4 whitespace-nowrap font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100"
                                        >{k[c]}</th
                                    >
                                {:else}
                                    <TableBodyCell>{k[c]}</TableBodyCell>
                                {/if}
                            {/each}
                        </TableBodyRow>
                    {/each}
                </TableBody>
            </Table>
        {/if}
    </div>
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Gene"
        triggeredBy="#click"
        trigger="click"
        placement="bottom"
        reference="#click">The name of the gene containing the exon</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Transcript"
        triggeredBy="#click2"
        trigger="click"
        placement="bottom"
        reference="#click2"
        >The name of the transcript containing the exon
    </Popover>
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Exon"
        triggeredBy="#click3"
        trigger="click"
        placement="bottom"
        reference="#click3">The unique name or number of the exon</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-100"
        title="Exon usage"
        triggeredBy="#click4"
        trigger="click"
        placement="bottom"
        reference="#click4"
        >1 if the exon is included in all transcripts</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Exon size"
        triggeredBy="#click5"
        trigger="click"
        placement="bottom"
        reference="#click5">The length of the target exon (in bp)</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Exon strand"
        triggeredBy="#click6"
        trigger="click"
        placement="bottom"
        reference="#click6">The direction of the exon (e.g., + or -)</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Chromosome"
        triggeredBy="#click7"
        trigger="click"
        placement="bottom"
        reference="#click7"
        >The name of the chromosome where the exon is located</Popover
    >
    <Popover
        arrow={false}
        class="w-64 text-sm font-light z-9999"
        title="Exon start"
        triggeredBy="#click8"
        trigger="click"
        placement="bottom"
        reference="#click8"
        >The start position of the exon (chromosomal coordinate)</Popover
    >
    <Popover
        arrow={false}
        class="w-64 text-sm font-light z-9999"
        title="Exon end"
        triggeredBy="#click9"
        trigger="click"
        placement="bottom"
        reference="#click9"
        >The end position of the exon (chromosomal coordinate)</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Cumulative CDS size"
        triggeredBy="#click10"
        trigger="click"
        placement="bottom"
        reference="#click10"
        >Cumulative coding sequence length in the transcript up to the current
        exon</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Total Coding size"
        triggeredBy="#click11"
        trigger="click"
        placement="bottom"
        reference="#click11"
        >The total coding sequence length of the transcript</Popover
    >

    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Insertion_sequence"
        triggeredBy="#click12"
        trigger="click"
        placement="bottom"
        reference="#click12"
        >Refers to the target sequence, either MAGR or VDGN</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Insertion_start"
        triggeredBy="#click13"
        trigger="click"
        placement="bottom"
        reference="#click13"
        >Start position of the target sequence
    </Popover>
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Insertion_end"
        triggeredBy="#click14"
        trigger="click"
        placement="bottom"
        reference="#click14">End position of the target sequence</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Left_remain"
        triggeredBy="#click15"
        trigger="click"
        placement="bottom"
        reference="#click15"
        >Length of the remaining sequence on the left when the target is cut
        (e.g., MAG|R or VDG|N)</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="Right_remain"
        triggeredBy="#click16"
        trigger="click"
        placement="bottom"
        reference="#click16"
        >Length of the remaining sequence on the right when the target is cut
        (e.g., MAG|R or VDG|N)</Popover
    >
    <Popover
        arrow={false}
        class="popover-fix w-64 text-sm font-light z-9999"
        title="n_editable"
        triggeredBy="#click19"
        trigger="click"
        placement="bottom"
        reference="#click19"
        >Number of CRISPR sgRNA target sequences available for inserting SCON to the target</Popover
    >

    <div class="p-3">
        <P size="xl" weight="semibold" class="py-3">Exon Info</P>

        <Table divClass="-z-10">
            <TableHead>
                <TableHeadCell>
                    <div id="click">Gene</div></TableHeadCell
                >
                <TableHeadCell id="click2">Transcript</TableHeadCell>
                <TableHeadCell id="click3">Exon</TableHeadCell>
                <TableHeadCell id="click4">Exon_usage</TableHeadCell>
                <TableHeadCell id="click5">Exon_size</TableHeadCell>
                <TableHeadCell id="click6">Exon_strand</TableHeadCell>
                <TableHeadCell id="click7">Chromosome</TableHeadCell>
                <TableHeadCell id="click8">Exon_start</TableHeadCell>
                <TableHeadCell id="click9">Exon_end</TableHeadCell>
                <TableHeadCell id="click10">Cumulative CDS size</TableHeadCell>
                <TableHeadCell id="click11">total coding size</TableHeadCell>
            </TableHead>
            {#if cexoninfo}
                <TableBody tableBodyClass="divide-y">
                    <TableBodyRow>
                        <TableBodyCell>
                            {cexoninfo[0].Gene}
                        </TableBodyCell>
                        <TableBodyCell>
                            {cexoninfo[0].Transcript}
                        </TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon_usage}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon_size}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon_strand}</TableBodyCell
                        >
                        <TableBodyCell>{cexoninfo[0].Chromosome}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon_start}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].Exon_end}</TableBodyCell>
                        <TableBodyCell>{cexoninfo[0].cum_size}</TableBodyCell>
                        <TableBodyCell
                            >{cexoninfo[0].coding_size_t}</TableBodyCell
                        >
                    </TableBodyRow>
                </TableBody>
            {/if}
        </Table>
    </div>
    <div class="p-3 z-0 w-full">
        <div class="flex items-center gap-2">
            <P size="xl" weight="semibold" class="py-3">Sequence browser</P>
            {#if isLoadingSequence}
                <Spinner size="6" color="green" />
            {/if}
        </div>

        {#if sequence && cexoninfo}
        <div class="relative">
            <div class="text-center text-gray-700 text-sm font-mono pb-2">
                Exon {cexoninfo[0].Exon} |
                chr{cexoninfo[0].Chromosome}:
                {Number(cexoninfo[0].Exon_strand) === -1
                  ? Number(cexoninfo[0].Exon_end).toLocaleString()
                  : Number(cexoninfo[0].Exon_start).toLocaleString()}
                -
                {Number(cexoninfo[0].Exon_strand) === -1
                  ? Number(cexoninfo[0].Exon_start).toLocaleString()
                  : Number(cexoninfo[0].Exon_end).toLocaleString()}
              </div>
            <!-- fixed legend box -->
            <div class="absolute top-3 left-3 z-50 bg-white border border-gray-300 p-3 rounded-md shadow-md text-sm space-y-1">
              <div><span class="text-gray-600 font-mono text-xs">5’ → 3’ direction</span></div>
              <div class="flex items-center gap-2">
                <span class="w-4 h-4 bg-red-700 inline-block rounded-sm"></span>
                <span class="text-gray-800">SCON Target (MAGR/VDGN)</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-4 h-4 bg-emerald-400 inline-block rounded-sm"></span>
                <span class="text-gray-800">PAM Sequence</span>
              </div>
            </div>
            <div class="overflow-x-auto">
                <div class="relative flex flex-col min-w-max font-mono text-[15px] max-h-[28em] overflow-y-auto">
    
                    <!-- BLACK BOX : Target position -->
                    {#each targetBoxes as box}
                        <div
                        class="absolute h-[0.33em] rounded-sm hover:cursor-pointer"
                        style="
                            left: calc(({box.start - sequence[0].pos}) * 1ch);
                            width: calc(({box.end - box.start + 1}) * 1ch);
                            top: calc(10em + {box.topOffset}em);
                        "
                        role="button"
                        tabindex="0"
                        on:mouseover={() => highlightFromBox(box.start, box.end)}
                        on:mouseout={handleRowMouseLeave}
                        on:focus={() => highlightFromBox(box.start, box.end)}
                        on:blur={handleRowMouseLeave}
                        >
                        <div class="absolute inset-0 bg-black rounded-sm"></div>
                    
                        {#if box.pam === "left"}
                            <div class="absolute left-0 w-[3ch] h-full bg-emerald-400 rounded-sm"></div>
                        {:else if box.pam === "right"}
                            <div class="absolute right-0 w-[3ch] h-full bg-emerald-400 rounded-sm"></div>
                        {/if}
                        </div>
                    {/each}
                    <!-- 100bp line + number -->
                    <div class="absolute top-0 left-0 flex w-full pointer-events-none h-[10em] z-20">
                        {#each sequence as s, i}
                        <div class="relative w-[1ch] text-center">
                            {#if s.pos % 100 === 0}
                            <div class="absolute bottom-0 left-1/2 -translate-x-1/2 h-[10em] w-[1px] bg-gray-500"></div>
                            <div class="absolute bottom-[10em] left-1/2 -translate-x-1/2 text-[10px] text-gray-500">
                                {s.pos}
                            </div>
                            {/if}
                        </div>
                        {/each}
                    </div>
                    <!-- 25bp dot line -->
                    <div class="absolute top-0 left-0 flex w-full pointer-events-none h-[10em] z-10">
                        {#each sequence as s (s.pos)}
                        <div class="relative w-[1ch] text-center">
                            {#if s.pos % 25 === 0 && s.pos % 100 !== 0}
                            <div class="absolute top-0 left-1/2 -translate-x-1/2 h-[2em] w-[1px] border-l border-dashed border-gray-400"></div>
                            {/if}
                        </div>
                        {/each}
                    </div>
                    <!-- sequence line -->
                    <div class="flex leading-none z-10 mt-[10em]">
                        {#each sequence as s}
                        <span
                            class="w-[1ch] text-center {getClassForBackground(s, hoveredRow, hoveredPAM)}"
                            class:font-bold={hoveredRow && s.pos >= hoveredRow.start && s.pos <= hoveredRow.end}
                            class:text-emerald-400={isPAMLetter(s.pos)}
                            class:text-red-700={s.className.includes("exon") && s.className.includes("scon_MAGR")}
                        >
                            {s.base}
                        </span>
                        {/each}
                    </div>
                <!-- chevron line -->
                <div class="flex leading-none text-gray-300 z-0">
                    {#each chevronTrack.split("") as c}
                    <span class="w-[1ch] text-center">{c}</span>
                    {/each}
                </div>
                </div>
            </div>
        </div>
        {/if}
        <div class="max-h-[40rem] overflow-y-auto">
            <div class="flex justify-end mb-2">
                <Button
                    class="text-sm px-3 py-1 rounded bg-green-600 text-white hover:bg-green-700"
                    on:click={downloadAllCSV}
                >
                    ⬇ Download table
                </Button>
            </div>
            <Table>
                <TableHead>
                    <TableHeadCell></TableHeadCell>
                    <TableHeadCell id="click12"
                        >Insertion_sequence</TableHeadCell
                    >
                    <TableHeadCell id="click13">Insertion_start</TableHeadCell>
                    <TableHeadCell id="click14">Insertion_end</TableHeadCell>
                    <TableHeadCell id="click15">Left_remain</TableHeadCell>
                    <TableHeadCell id="click16">Right_remain</TableHeadCell>
                    <TableHeadCell id="click19">n_editable</TableHeadCell>
                </TableHead>
                {#if sequence && cexoninfo}
                    {#each cexoninfo as c, i}
                        <TableBody tableBodyClass="divide-y w-full">
                            <tr
                                on:blur={handleRowMouseLeave}
                                on:focus={() =>
                                    handleRowMouseEnter(
                                        i,
                                        c.Insertion_start,
                                        c.Insertion_end,
                                    )}
                                on:mouseover={() =>
                                    handleRowMouseEnter(
                                        i,
                                        c.Insertion_start,
                                        c.Insertion_end,
                                        c.scon_sites,
                                        Number(cexoninfo[0]?.Exon_strand || 1),
                                    )}
                                on:mouseout={handleRowMouseLeave}
                            >
                                <td
                                    on:click={() => toggleClick(i)}
                                    class="px-6 py-4 whitespace-nowrap font-medium text-gray-900 dark:text-white cursor-pointer hover:bg-gray-100"
                                >
                                    <ChevronDownOutline />
                                </td>
                                <TableBodyCell id="click12"
                                    >{c.Insertion_sequence}</TableBodyCell
                                >
                                <TableBodyCell id="click13"
                                    >{c.Insertion_start}</TableBodyCell
                                >
                                <TableBodyCell id="click14"
                                    >{c.Insertion_end}</TableBodyCell
                                >
                                <TableBodyCell id="click15"
                                    >{c.Left_remain}</TableBodyCell
                                >
                                <TableBodyCell id="click16"
                                    >{c.Right_remain}</TableBodyCell
                                >
                                <TableBodyCell id="click12"
                                    >{c.n_editable}</TableBodyCell
                                >
                            </tr>

                            {#if clickedRows[i]}
                                <TableBodyRow class="bg-gray-100">
                                    <TableBodyCell colspan="11">
                                        <div class="flex items-start gap-4">
                                            <div class="min-w-max pt-1">
                                                <Button
                                                    class="text-sm px-2 py-1 mb-2 bg-green-500 text-white hover:bg-green-600 rounded"
                                                    on:click={() => downloadHomologyArmsSingle(c)}
                                                >
                                                    🧬Download ssODN
                                                </Button>
                                            </div>
                                        <div class="inner-table-container pl-5">
                                            <Table class="inner-table">
                                                <TableHead>
                                                    <TableHeadCell id="click20"
                                                        >PAM_position</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click21"
                                                        >Target_sequence</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click22"
                                                        >Target_length</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click23"
                                                        >Target_start</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click24"
                                                        >Target_end</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click17"
                                                        >GC</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click18"
                                                        >Self_complement</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click25"
                                                        >mm_score</TableHeadCell
                                                    >
                                                    <TableHeadCell id="click26"
                                                        >in_frame</TableHeadCell
                                                    >
                                                </TableHead>
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="PAM_position"
                                                    triggeredBy="#click20"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click20"
                                                    >Position of the PAM
                                                    sequence relative to the
                                                    CRISPR sgRNA sequence</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="Target_sequence"
                                                    triggeredBy="#click21"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click21"
                                                    >CRISPR sgRNA sequence</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="Target_length"
                                                    triggeredBy="#click22"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click22"
                                                    >Length of the CRISPR sgRNA
                                                    sequence</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="Target_start"
                                                    triggeredBy="#click23"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click23"
                                                    >Start position of the
                                                    CRISPR sgRNA sequence</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="Target_end"
                                                    triggeredBy="#click24"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click24"
                                                    >End position of the CRISPR
                                                    sgRNA sequence</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="mm_score"
                                                    triggeredBy="#click25"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click25"
                                                    >Mismatch score indicating
                                                    how frequently the CRISPR
                                                    sgRNA sequence maps to
                                                    the entire sequence (MM0,MM1,MM2)</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="GC"
                                                    triggeredBy="#click17"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click17"
                                                    >GC content of the CRISPR
                                                    sgRNA sequence for
                                                    cutting the target</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="Self_complement"
                                                    triggeredBy="#click18"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click18"
                                                    >Number of possible occurrences where the CRISPR sgRNA sequence
                                                    forms a secondary hairpin structure</Popover
                                                >
                                                <Popover
                                                    arrow={false}
                                                    class="popover-fix w-64 text-sm font-light z-9999 text-wrap"
                                                    title="In_frame"
                                                    triggeredBy="#click26"
                                                    trigger="click"
                                                    placement="bottom"
                                                    reference="#click26"
                                                    >Whether the coding sequence remains in frame or 
                                                    shifts the reading frame when alternative splicing occurs
                                                    </Popover
                                                >
                                                {#each c.scon_sites as ss}
                                                    <TableBody
                                                        tableBodyClass="divide-y"
                                                    >
                                                        <tr class="bg-white">
                                                            <TableBodyCell
                                                                >{ss.PAM_position}</TableBodyCell
                                                            >
                                                            <td
                                                                class="px-6 py-4 whitespace-nowrap font-medium text-gray-900 dark:text-white"
                                                                on:blur={handleRowMouseLeave}
                                                                on:focus={() =>
                                                                    handleRowMouseEnter(
                                                                        i,
                                                                        c.Insertion_start,
                                                                        c.Insertion_end,
                                                                    )}
                                                                on:click={() =>
                                                                    handleRowMouseEnter(
                                                                        i,
                                                                        c.Insertion_start,
                                                                        c.Insertion_end,
                                                                        [
                                                                            {
                                                                                Tartget_start:
                                                                                    ss.Tartget_start,
                                                                                Tartget_end:
                                                                                    ss.Tartget_end,
                                                                            },
                                                                        ],
                                                                    )}
                                                                >{ss.Target_sequence}</td
                                                            >
                                                            <TableBodyCell
                                                                >{ss.Target_length}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss.Tartget_start}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss.Tartget_end}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss.GC}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss.Self_complement}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss.MM_score}</TableBodyCell
                                                            >
                                                            <TableBodyCell
                                                                >{ss[
                                                                    "3N"
                                                                ]}</TableBodyCell
                                                            >
                                                        </tr>
                                                    </TableBody>
                                                {/each}
                                            </Table>
                                            </div>
                                        </div>
                                    </TableBodyCell>
                                </TableBodyRow>
                            {/if}
                        </TableBody>
                    {/each}
                {/if}
            </Table>
        </div>
    </div>
</div>

<style>
    .suggestions-list {
        max-height: 150px;
        width: 500px;
        overflow-y: auto;
    }
    .suggestion-list {
        max-height: 150px;
        width: 280px;
        overflow-y: auto;
    }
    .placeholder-white::placeholder {
        color: white;
    }
    .inner-table-container {
        width: 100%;
        overflow-x: auto;
        z-index: 0 !important;
        position: relative !important;
    }
    .inner-table {
        width: 100%;
        border-collapse: collapse;
        position: relative;
        z-index: 0;
    }
    .inner-table th,
    .inner-table td {
        border: 1px solid #e5e7eb;
        padding: 0.5rem;
    }
    .outer-table {
        width: 100%;
    }

    .popover-fix {
        position: fixed !important;
        z-index: 9999 !important; 
    }

    .max-h-\[40rem\] {
        position: relative;
        z-index: 0 !important;
    }
    @import "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css";
</style>
