<script>
  import { Heading, P } from "flowbite-svelte";
  import { page } from "$app/stores";
  import {
      Sidebar,
      SidebarGroup,
      SidebarItem,
      SidebarWrapper,
      Button,
      Navbar,
      NavBrand,
      NavLi,
      NavUl,
      NavHamburger,
  } from "flowbite-svelte";
  $: activeUrl = $page.url.pathname;
  let activeClass =
      "text-white font-semibold bg-green-700 md:bg-transparent md:text-green-700 md:dark:text-white dark:bg-green-600 md:dark:bg-transparent";
  let nonActiveClass =
      "text-gray-700 hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-green-700 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent";
</script>


<div class="w-full px-4 py-10">
  <div class="max-w-[1800px] min-w-[768px] mx-auto">
    <div class="w-full border-b border-gray-300 mb-4 pb-2">
      <Heading size="2xl" class="text-gray-800 font-bold text-left px-6">
        GENPOS-SCONDB
      </Heading>
    </div>
    <div class="mt-5 p-10 bg-green-100 rounded-lg">
      <Heading size="3xl" class="text-center font-extrabold text-green-700 mb-6">
        Design conditional knock‑outs in&nbsp;<i>300+</i>&nbsp;vertebrate.<br />
      </Heading>
      <P size="xl" class="text-center text-gray-700 mb-4">
        <i>"Single injection, hundreds of species."</i>
      </P>
      <P size="lg" class="max-w-3xl mx-auto text-gray-700">
        <b>SCON (Short Conditional intrON)</b> is a next-generation tool that radically simplifies functional genetic studies. 
        With just a 189-bp sequence, SCON enables conditional intron functionality across various vertebrate species. 
        A single insertion allows fast and powerful generation of conditional alleles — all without the complexity of traditional floxed systems.
      </P>
      <div class="flex justify-center">
        <Button color="green" size="lg" class="mt-8 px-8" href="/analysis">
          Launch the online designer →
        </Button>
      </div>
    </div>
    <div class="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 p-6">
      <!-- Card 1 -->
      <div class="bg-white shadow-md rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition">
        <img src="/SCON_paper_1.png" alt="SCON loxP Figure" class="w-full h-[360px] object-cover bg-gray-50 p-2" />
        <div class="p-4 flex flex-col h-full">
          <h3 class="text-lg font-bold text-gray-800 mb-2">
            SCON—a Short Conditional intrON for conditional knockout
          </h3>
          <p class="text‑sm text‑gray‑500 mb‑4">
            <em>Experimental & molecular medicine 2022</em>
          </p>
          <p class="text-sm text-gray-600 mb-3 line-clamp-5">
            The generation of conditional alleles using CRISPR technology is still challenging. Here, we introduce a Short Conditional intrON (SCON, 189 bp) that enables the rapid generation of conditional alleles via one-step zygote injection...
          </p>
          <ul class="text-sm text-gray-500 list-disc ml-5 mb-4">
            <li>One-step zygote injection</li>
            <li>13 mouse lines generated</li>
            <li>MAGR/VDGN site tagetable</li>
          </ul>
          <div class="flex justify-end">
            <Button color="green" size="sm" class="mt-8 px-8" href="https://doi.org/10.1038/s12276-022-00891-0">
              Go to paper →
            </Button>
          </div>
        </div>
      </div>
    
      <!-- Card 2 -->
      <div class="bg-white shadow-md rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition">
        <img src="/SCON_paper_2.png" alt="Red2Flpe-SCON Figure" class="w-full h-[360px] object-cover bg-gray-50 p-2" />
        <div class="p-4 flex flex-col h-full">
          <h3 class="text-lg font-bold text-gray-800 mb-2">
            Red2Flpe-SCON: Multicolor Conditional Knockout Mice
          </h3>
          <p class="text‑sm text‑gray‑500 mb‑4">
            <em>Nature Communications 2024</em>
          </p>
          <p class="text-sm text-gray-600 mb-3 line-clamp-5">
            Red2Flpe-SCON: a mosaic knockout system that uses multicolor reporters to label both mutant and wild-type cells. This enables analysis of gene function at clonal resolution...
          </p>
          <ul class="text-sm text-gray-500 list-disc ml-5 mb-4">
            <li>Red-only Flpe expression system</li>
            <li>FRT-based SCON integration</li>
            <li>Used in Sox2 clonal analysis</li>
          </ul>
          <div class="flex justify-end">
            <Button color="green" size="sm" class="mt-8 px-8" href="https://doi.org/10.1038/s41467-024-49382-y">
              Go to paper →
            </Button>
          </div>
        </div>
      </div>
    
      <!-- Card 3 -->
      <div class="relative bg-white shadow-md rounded-lg overflow-hidden border border-gray-200 hover:shadow-lg transition opacity-50">
        <div class="absolute inset-0 bg-white bg-opacity-100 flex items-center justify-center z-10">
          <span class="text-lg font-semibold text-gray-800"> Coming Soon...</span>
        </div>
        <img src="/SCON_paper_3.png" alt="universal SCON Figure" class="w-full h-[360px] object-cover bg-gray-50 p-2" />
        <div class="p-4 flex flex-col h-full">
          <h3 class="text-lg font-bold text-gray-800 mb-2">
            Universal Conditional Knockout in Fish & Human iPSCs
          </h3>
          <p class="text-sm text-gray-500 mb-4"><em>2025</em></p>
          <p class="text-sm text-gray-600 mb-3 line-clamp-5">
            This study introduces a broadly applicable approach to generate conditional loss-of-function mutations in zebrafish, iPSCs, and organoids using a streamlined SCON system...
          </p>
          <ul class="text-sm text-gray-500 list-disc ml-5 mb-4">
            <li>Cross-species SCON compatibility</li>
            <li>Essential-gene-safe cassette</li>
            <li>Organoid & human iPSC tested</li>
            <li>Web-based knockout design tool</li>
          </ul>
          <a href="#" class="text-green-600 hover:text-green-800 font-medium mt-auto pointer-events-none">📄 View paper</a>
        </div>
      </div>
    </div>

        <div class="grid grid-cols-1 md:grid-cols-[minmax(100px,550px)_1fr] gap-4 mt-5">
    
          <!-- Left: Database overview -->
          <div class="p-10 bg-green-100 rounded-lg">
            <P size="2xl" weight="bold" class="text-gray-800 mb-4">Database overview</P>
            <img src="/scondb_overview2.svg" alt="overview_Img" class="w-full h-auto object-contain" />
          </div>
        
          <!-- Right: Statistics -->
          <div class="p-10 bg-green-100 rounded-lg">
            <P size="2xl" weight="bold" class="text-gray-800 mb-4">Statistics</P>
            <img src="/statistics.png" alt="SCON Statistics" class="w-full h-auto object-contain" />
          </div>
      
        <!-- Bottom Full-Width: Release Note -->
        <div class="p-10 bg-green-100 rounded-lg col-span-2">
          <P size="2xl" weight="bold" class="text-gray-800 mb-4">Release Note</P>
          <div class="flex flex-row mb-2">
            <P size="md" weight="medium" class="w-32">2024.10.15</P>
            <P class="flex-1">Draft version publish</P>
          </div>
          <div class="flex flex-row">
            <P size="md" weight="medium" class="w-32">2025.04.17</P>
            <P class="flex-1">v1.0.0 First release</P>
          </div>
        </div>
      </div>
      <!-- Footer -->
      <footer class="bg-gray-100 w-full py-10 border-t border-gray-300 mt-10">
        <div class="max-w-screen-xl px-6 text-sm text-gray-700 text-left">
          <h4 class="text-base font-semibold mb-2">Citation</h4>
          <p class="mb-1">
            <a href="https://doi.org/10.1038/s12276-022-00891-0" target="_blank" rel="noopener noreferrer"
              class="text-green-700 hover:underline">
              Wu, SH.S., et al. SCON—a Short Conditional intrON for conditional knockout. <em>Exp Mol Med</em> (2022).
            </a>
          </p>
          <p class="mb-1">
            <a href="https://doi.org/10.1038/s41467-024-49382-y" target="_blank" rel="noopener noreferrer"
              class="text-green-700 hover:underline">
              Wu, SH.S., et al. Red2Flpe-SCON: strategy for mosaic knockout mice. <em>Nat Commun</em> (2024).
            </a>
          </p>
          <h4 class="text-base font-semibold mb-2">GitHub</h4>
          <p class="mb-1">
            <a href="https://github.com/bis-lab/scondb" target="_blank" rel="noopener noreferrer"
              class="text-green-700 hover:underline font-medium">
              github.com/bis-lab/scondb
            </a>
          </p>
          <p class="mt-4 text-gray-500">© 2025 BIS-Lab, CGE, IBS. All rights reserved.</p>
        </div>
      </footer>
  </div>
</div>