/** @format */

console.log("init");
const socket = io("wss://etd.monitor.sirileepage.com/clients");

socket.on("history", (data) => {
  const block_time_display = document.querySelector("#num_block_time");
  const block_number_display = document.querySelector("#num_blocks");
  const network_hashrate_display = document.querySelector("#num_hash_rate");

  const blockTime = data.latestAvgBlockTime;
  const difficulty = data.latestDifficulty;
  const blockNumber = data.latestBlockNumber;

  console.log(blockTime, difficulty, blockNumber);
  const networkHashRate = difficulty / blockTime;

  block_number_display.innerHTML = `${blockNumber}`;
  block_time_display.innerHTML = `${blockTime} s`;
  network_hashrate_display.innerHTML = `${networkHashRate.toFixed(0)}`;
});
