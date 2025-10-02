document.addEventListener('DOMContentLoaded', () => {
  const signalsContainer = document.getElementById('signals-container');
  const statusDiv = document.createElement('div');
  signalsContainer.appendChild(statusDiv);

  const updateStatus = (message, isError = false) => {
    statusDiv.textContent = message;
    statusDiv.style.color = isError ? 'red' : 'black';
  };

  updateStatus('Connecting to WebSocket...');

  const ws = new WebSocket('ws://localhost:5000');

  ws.onopen = () => {
    console.log('WebSocket connection established.');
    updateStatus('Connected. Waiting for signals...');
  };

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data);
      if (message.type === 'signal' && message.data) {
        updateStatus('New signal received!');
        displaySignal(message.data);
      } else if (message.type === 'welcome') {
        console.log('Welcome message received:', message.message);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    updateStatus('Connection error. Is the server running?', true);
  };

  ws.onclose = () => {
    console.log('WebSocket connection closed.');
    updateStatus('Connection closed.', true);
  };

  const displaySignal = (signal) => {
    // Clear previous signals
    signalsContainer.innerHTML = '';

    const signalElement = document.createElement('div');
    signalElement.className = 'signal';

    const signalAction = document.createElement('h2');
    signalAction.textContent = `${signal.signal} ${signal.symbol}`;
    signalAction.style.color = signal.signal === 'BUY' ? 'green' : 'red';

    const signalDetails = document.createElement('ul');

    const createListItem = (key, value) => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${key}:</strong> ${value}`;
      return li;
    };

    signalDetails.appendChild(createListItem('Entry Price', signal.entryPrice));
    signalDetails.appendChild(createListItem('Stop Loss', signal.stopLoss));
    signalDetails.appendChild(createListItem('Target Price', signal.targetPrice));
    signalDetails.appendChild(createListItem('Confidence', signal.confidence));

    signalElement.appendChild(signalAction);
    signalElement.appendChild(signalDetails);

    // Prepend the new signal so it appears at the top
    signalsContainer.prepend(signalElement);
  };
});