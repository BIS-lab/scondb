<script>
    import { page } from "$app/stores";
    import "../app.css";
    import {
        Sidebar,
        SidebarGroup,
        SidebarItem,
        SidebarWrapper,
    } from "flowbite-svelte";

    let activeClass =
        "flex items-center p-2 text-base font-normal text-primary-900 bg-primary-200 dark:bg-primary-700 rounded-lg dark:text-white hover:bg-primary-100 dark:hover:bg-gray-700";
    let nonActiveClass =
        "flex items-center p-2 text-base font-normal text-green-900 rounded-lg dark:text-white hover:bg-green-100 dark:hover:bg-green-700";
    
    let open = true;
</script>

<div class="flex h-screen w-full overflow-hidden bg-white dark:bg-gray-900">
    
    {#if open}
        <aside class="h-full flex-none border-r border-gray-200 dark:border-gray-700 relative">
            
            <button
                class="absolute -right-3 top-2 z-50 bg-green-500 hover:bg-green-600 rounded-full w-6 h-10 font-bold text-white shadow-md"
                on:click={() => { open = false; }}>
                {"<"}
            </button>

            <Sidebar class="w-fit h-full" {activeClass} {nonActiveClass}>
                <SidebarWrapper
                    class="py-10 h-full overflow-y-auto px-3"
                >
                    <SidebarGroup>
                        <SidebarItem
                            label="Home"
                            href="/"
                            active={$page.url.pathname === "/"}
                        ></SidebarItem>
                        <SidebarItem
                            label="Dataset"
                            href="/dataset"
                            active={$page.url.pathname === "/dataset"}
                        ></SidebarItem>
                        <SidebarItem
                            label="Analysis"
                            href="/analysis"
                            active={$page.url.pathname === "/analysis"}
                        ></SidebarItem>
                        <SidebarItem
                            label="Tutorial"
                            href="/tutorial"
                            active={$page.url.pathname === "/tutorial"}
                        ></SidebarItem>
                        <SidebarItem
                            label="About SCON"
                            href="/about"
                            active={$page.url.pathname === "/about"}
                        ></SidebarItem>
                    </SidebarGroup>
                </SidebarWrapper>
            </Sidebar>
        </aside>
    {:else}
        <button
            class="fixed left-0 top-2 z-50 bg-green-500 hover:bg-green-600 rounded-r-full w-6 h-10 font-bold text-white shadow-md"
            on:click={() => { open = true; }}>
            {">"}
        </button>
    {/if}

    <main class="flex-1 h-full overflow-y-auto">
        <div class="p-4">
            <slot />
        </div>
    </main>
</div>