<script lang="ts">
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { writable } from 'svelte/store';
	import type { Game, DecisionNode } from '$lib/types';

	export let data: PageData;

	const gameState = writable<Game | null>(data.game);
	const decisionNodeState = writable<DecisionNode | null>(data.decisionNode);
	const narrativeState = writable<string | null>(data.game?.last_narrative || null);

	let isLoadingDecision = false;
	let socket: WebSocket | null = null;

	onMount(() => {
		const gameId = $gameState?.id;
		if (!gameId) return;

		const wsUrl = `ws://localhost:8000/ws/${gameId}`;
		socket = new WebSocket(wsUrl);

		socket.onopen = () => console.log('WebSocket connection established.');
		socket.onmessage = (event) => {
			const message = event.data as string;
			if (message.startsWith('NARRATIVE_READY:')) {
				const newNarrative = message.substring('NARRATIVE_READY:'.length);
				narrativeState.set(newNarrative);
				decisionNodeState.set(null);
			}
		};
        // ... (other WebSocket handlers)
		return () => socket?.close();
	});

	async function handleDecision(optionId: number) {
		isLoadingDecision = true;
        narrativeState.set("وقایع‌نگار در حال ثبت تاریخ است...");
        decisionNodeState.set(null); 

		try {
			const currentGame = $gameState;
			if (!currentGame) return;

			const response = await fetch(`http://localhost:8000/api/v1/games/${currentGame.id}/decide`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ option_id: optionId })
			});

			if (!response.ok) throw new Error( (await response.json()).detail );
			const updatedGame: Game = await response.json();
			gameState.set(updatedGame);
		} catch (error) {
			if (error instanceof Error) alert(`خطا: ${error.message}`);
			else alert('یک خطای ناشناخته رخ داد');
		} finally {
			isLoadingDecision = false;
		}
	}

    /**
     * Fetches the next decision node based on the current game state.
     */
    async function proceedToNextDecision() {
        isLoadingDecision = true;
        narrativeState.set(null); // Clear the narrative
        
        const nextNodeId = $gameState?.current_decision_node_id;
        if(nextNodeId) {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/decisions/${nextNodeId}`);
                if (!response.ok) throw new Error("مرحله بعدی داستان یافت نشد.");
                const nextNode = await response.json();
                decisionNodeState.set(nextNode);
            } catch (error) {
                 if (error instanceof Error) alert(`خطا: ${error.message}`);
			     else alert('یک خطای ناشناخته رخ داد');
            }
        } else {
            // This is already handled by the main #if block, but good for safety
            decisionNodeState.set(null);
        }
        isLoadingDecision = false;
    }

    function getStatusColor(value: number): string {
        if (value < 30) return 'bg-red-600';
        if (value < 70) return 'bg-yellow-500';
        return 'bg-green-500';
    }
</script>

<div class="min-h-screen p-4 sm:p-8 flex flex-col items-center font-serif">
	<!-- Header / Resource Bar -->
    {#if $gameState}
	<header class="w-full max-w-7xl mb-8">
        <!-- ... (Resource bar HTML remains the same) ... -->
	</header>
    {/if}

	<!-- Main Decision/Narrative Area -->
	<main class="w-full max-w-4xl">
        {#if $decisionNodeState}
            <!-- Decision Card -->
            <div class="bg-black/20 p-8 rounded-2xl border border-primary/20">
                <p class="text-2xl leading-loose text-primary/90 mb-8 text-justify">
                    {$decisionNodeState.node_text}
                </p>
                <div class="border-t border-accent/30 pt-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-xl text-accent font-bold">گزینه‌های پیش رو:</h3>
                        <button class="bg-white/10 text-primary/80 px-4 py-2 rounded-lg text-sm hover:bg-white/20 transition-colors" title="این قابلیت به زودی اضافه خواهد شد">
                            مشورت با شورا
                        </button>
                    </div>
                    <div class="space-y-4">
                        {#each $decisionNodeState.options as option}
                            <button
                                on:click={() => handleDecision(option.id)}
                                disabled={isLoadingDecision}
                                class="w-full text-right bg-white/5 hover:bg-white/10 p-4 rounded-lg
                                       border border-primary/20 transition-colors duration-200
                                       disabled:opacity-50 disabled:cursor-wait"
                            >
                                <span class="text-lg text-primary">{option.option_text}</span>
                            </button>
                        {/each}
                    </div>
                </div>
            </div>
        {:else if $narrativeState}
            <!-- Narrative Display -->
            <div class="bg-primary/5 p-8 rounded-lg border-2 border-dashed border-accent/30 animate-fade-in">
                 <h3 class="text-xl text-accent mb-4 font-bold">روایت وقایع...</h3>
                 <p class="text-2xl leading-loose text-primary text-justify">
                    {$narrativeState}
                 </p>
                 <div class="text-center mt-8">
                    <button 
                        on:click={proceedToNextDecision}
                        class="bg-accent text-background font-bold text-lg py-2 px-8 rounded-lg
                               hover:bg-accent-hover transform hover:scale-105 transition-all"
                    >
                        ادامه ماجراجویی
                    </button>
                 </div>
            </div>
        {:else}
            <!-- End of Branch Display -->
            <div class="text-center p-8 bg-black/20 rounded-2xl">
                <!-- ... (end of history message remains the same) ... -->
            </div>
        {/if}
	</main>
</div>

<style>
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in {
        animation: fade-in 0.5s ease-out forwards;
    }
</style>
