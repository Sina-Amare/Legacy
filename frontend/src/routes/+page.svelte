<script lang="ts">
	import { onMount } from 'svelte';
	import type { Dynasty } from '$lib/types';

	let dynastiesPromise: Promise<Dynasty[]>;

	/**
	 * Formats a historical year for display, adding BCE (ق.م) or CE (م) labels.
	 * @param year The year to format, which can be negative.
	 */
	function formatYear(year: number): string {
		if (year < 0) {
			return `${Math.abs(year)} ق.م`;
		}
		return `${year} م`;
	}

	onMount(() => {
		dynastiesPromise = fetch('http://localhost:8000/api/v1/dynasties').then((res) => {
			if (!res.ok) throw new Error('بارگذاری اطلاعات از سرور با مشکل مواجه شد');
			return res.json();
		});
	});
</script>

<div class="min-h-screen p-4 sm:p-8 flex flex-col items-center">
	<header class="text-center mb-12">
		<h1 class="text-6xl font-bold text-primary tracking-wider font-serif">میراث</h1>
		<p class="text-xl text-primary/70 mt-2 font-serif">تاریخ‌ را از نو بسازید</p>
	</header>

	<main class="max-w-4xl w-full">
		<h2 class="text-3xl font-bold text-accent border-b-2 border-accent/30 pb-2 mb-8 font-serif">
			یک سلسله را برای شروع انتخاب کنید
		</h2>

		{#await dynastiesPromise}
			<div class="text-center text-primary/60 text-lg font-serif">
				در حال بارگذاری سرگذشت‌ها...
			</div>
		{:then dynasties}
			<div class="space-y-8">
				{#each dynasties as dynasty}
					<a
						href="/play/{dynasty.id}"
						class="block bg-white/5 rounded-2xl shadow-lg overflow-hidden 
                               transform transition-all duration-300 ease-in-out
                               hover:shadow-2xl hover:shadow-accent/20 hover:scale-[1.02]"
					>
						<div class="flex flex-col sm:flex-row h-74">
							<div class="sm:w-1/3 h-full">
								<img
									src={dynasty.image_url}
									alt={dynasty.name}
									class="w-full h-full object-cover"
								/>
							</div>

							<div class="sm:w-2/3 p-6 flex flex-col">
								<h3 class="text-3xl font-bold text-accent-hover mb-2 font-serif">
									{dynasty.name}
								</h3>
								<p class="text-md text-primary/70 mb-4 font-serif">
									{formatYear(dynasty.start_year)} - {formatYear(dynasty.end_year)}
								</p>
								<p class="text-primary/90 leading-relaxed flex-grow line-clamp-3">
									{dynasty.description}
								</p>
								<div class="text-left mt-auto pt-4">
									<span
										class="inline-block text-background bg-accent hover:bg-accent-hover font-bold py-2 px-6 rounded-lg transition-colors"
									>
										ورود به دوران
									</span>
								</div>
							</div>
						</div>
					</a>
				{/each}
			</div>
		{:catch error}
			<p class="text-center text-red-500 font-serif">
				{#if error instanceof Error}
					خطا در دریافت اطلاعات: {error.message}
				{:else}
					خطا در دریافت اطلاعات: یک مشکل ناشناخته رخ داد
				{/if}
			</p>
		{/await}
	</main>
</div>