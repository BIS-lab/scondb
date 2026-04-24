<script>
    import { onMount, onDestroy } from "svelte";
    import { load } from "../../lib/fetch";
    import { page } from "$app/stores";
    import {
        Table,
        TableBody,
        TableBodyCell,
        TableBodyRow,
        TableHead,
        TableHeadCell,
        Heading,
        GradientButton,
        Button,
        Search,
        Input,
        InputAddon,
        ButtonGroup,
        Dropdown,
        DropdownItem,
    } from "flowbite-svelte";
    import { selectedSpecies, push, selectedtype } from "../../lib/stores";
    import { ChevronDownOutline, SearchOutline } from "flowbite-svelte-icons";
    let dataset = [];
    let mounted = false;
    let s_species = "";
    let filteredDataset = [];
    let type = "VDGN";
    let isDropdownOpen = false;

    function goToAnalysis(species, type) {
        selectedSpecies.set(species);
        selectedtype.set(type);
        push.set(true);
    }

    function handleSelectInput(event) {
        s_species = event.target.value;
        updatedataset();
    }

    function updatedataset() {
        if (s_species) {
            filteredDataset = dataset.filter((item) =>
                item.species.toLowerCase().includes(s_species.toLowerCase()),
            );
        } else {
            filteredDataset = [];
        }
    }

    $: sortedDataset = [
        ...filteredDataset,
        ...dataset.filter((item) => !filteredDataset.includes(item)),
    ];

    $: if (type) {
        loadDatasetByType();
    }

    async function loadDatasetByType() {
        push.set(false);
        const rtn = await load(`meta/dataset?type=${type}`);
        dataset = rtn;
        mounted = true;
        updatedataset();
    }

    onMount(async () => {
        await loadDatasetByType();
    });
</script>

<div class="p-10 w-full px-8">
    <div class="w-full border-b border-gray-300 mb-4 pb-2">
        <Heading size="2xl" class="text-gray-800 font-bold text-left px-6">
          Available dataset
        </Heading>
      </div>
    <ButtonGroup class="w-full flex py-3 p-3">
        <Button
            color="none"
            class="flex-shrink-0 text-white bg-green-500 border border-gray-300 dark:border-gray-700 dark:text-white hover:bg-green-800 focus:ring-gray-300 dark:bg-gray-600 dark:hover:bg-gray-700 dark:focus:ring-gray-800"
        >
            {type}<ChevronDownOutline class="w-6 h-6 ms-2" />
        </Button>

        <Dropdown bind:open={isDropdownOpen}>
            <DropdownItem
                on:click={() => (type = "VDGN") && (isDropdownOpen = false)}
                >VDGN</DropdownItem
            >
            <DropdownItem
                on:click={() => (type = "MAGR") && (isDropdownOpen = false)}
                >MAGR</DropdownItem
            >
        </Dropdown>

        <Input
            placeholder="Search species"
            bind:value={s_species}
            on:input={handleSelectInput}
            class="disabled:cursor-not-allowed disabled:opacity-50 focus:border-green-400 focus:ring-green-400 dark:focus:border-green-400 dark:focus:ring-green-400 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 text-sm"
        />
        <Button class="bg-green-500 !p-2.5" color="primary" type="submit">
            <SearchOutline class="w-5 h-5" />
        </Button>
    </ButtonGroup>

    <!--<form class="">
        <Search
            size="md"
            bind:value={s_species}
            placeholder="Search Species"
            on:input={handleSelectInput}
            class="disabled:cursor-not-allowed disabled:opacity-50 focus:border-green-400 focus:ring-green-400 dark:focus:border-green-400 dark:focus:ring-green-400 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border-gray-300 text-sm"
        />
    </form>--->
    {#if mounted}
        <div class="px-3">
            <Table>
                <TableHead>
                    <TableHeadCell>Species</TableHeadCell>
                    <TableHeadCell>Ensembl version</TableHeadCell>
                    <TableHeadCell>Dataset</TableHeadCell>
                    <TableHeadCell></TableHeadCell>
                </TableHead>
                <TableBody tableBodyClass="divide-y">
                    {#each sortedDataset as s}
                        <tr
                            class={filteredDataset.includes(s)
                                ? "border-b last:border-b-0 border-green-400 bg-green-100"
                                : "border-b last:border-b-0 border-green-400 "}
                        >
                            <TableBodyCell>{s.species}</TableBodyCell>
                            <TableBodyCell>{s.ensemble_rev}</TableBodyCell>
                            <TableBodyCell>{s.name}</TableBodyCell>
                            <TableBodyCell>
                                <GradientButton
                                    class="m-1"
                                    outline
                                    color="tealToLime"
                                    href="/analysis"
                                    active={$page.url.pathname === "/analysis"}
                                    on:click={() =>
                                        goToAnalysis(s.species, type)}
                                >
                                    Go to Analysis
                                </GradientButton>
                            </TableBodyCell>
                        </tr>
                    {/each}
                </TableBody>
            </Table>
        </div>
    {/if}
</div>

<style>
    .highlight {
        background-color: #d1fae5; /* Tailwind CSS 연한 초록색 */
    }
</style>
