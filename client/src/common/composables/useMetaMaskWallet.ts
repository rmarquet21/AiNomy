import { onMounted, onUnmounted } from 'vue-demi'
import Web3 from "web3";

declare global {
  interface Window {
    ethereum: any
    web3: any
  }
}

// Wallet Connection and Utility functions

const isMetaMask: boolean
  = typeof window.ethereum !== 'undefined' && window.ethereum.isMetaMask

/**
 * Returns account address array if wallet is connected otherwise opens MetaMask popup.
 * On error, returns a single string with the error message
 */
async function connect() {
  if (isMetaMask) { 
    try {
      await initWeb3()
      const result: string[] = await window.ethereum.request({
        method: 'eth_requestAccounts',
      })
      return result
    }
    catch (e: any) {
      return `Error: Unable to execute request: ${e.message}`
    }
  }
  else {
    return 'Error: MetaMask not detected'
  }
}

/**
 * Get all connected accounts addresses. Returns an empty array if none connected
 * On error, returns a single string with the error message
 */
async function getAccounts() {
  if (isMetaMask) {
    try {
      const result: string[] = await window.ethereum.request({
        method: 'eth_accounts',
      })
      return result
    }
    catch (e: any) {
      return `Error: Unable to execute request: ${e.message}`
    }
  }
  else {
    return 'Error: MetaMask not detected'
  }
}

/**
 * Opens a MetaMask popup to connect/disconnect from a list of user's accounts.
 * Returns an array.
 * The popup opens even if the user has already connected some accounts.
 * On error, returns a single string with the error message
 */
async function switchAccounts() {
  if (isMetaMask) {
    try {
      const result: string[] = await window.ethereum.request({
        method: 'wallet_requestPermissions',
        params: [
          {
            eth_accounts: {},
          },
        ],
      })
      return result
    }
    catch (e: any) {
      return `Error: Unable to execute request: ${e.message}`
    }
  }
  else {
    return 'Error: MetaMask not detected'
  }
}

// Event handlers
/**
 * Event handler for when the user changes the account in MetaMask
 *
 * Reference for event handlers: https://docs.metamask.io/guide/ethereum-provider.html#events
 * @param callback Function that takes accounts string array as an argument
 */
export const onAccountsChanged = (callback: (accounts: string[]) => void) => {
  if (isMetaMask) {
    onMounted(() => {
      window.ethereum.on('accountsChanged', callback)
    })
    onUnmounted(() => {
      window.ethereum.removeListener('accountsChanged', callback)
    })
  }
}

/**
 * Event handler for when the user changes the active chain in MetaMask
 *
 * Reference for event handlers: https://docs.metamask.io/guide/ethereum-provider.html#events
 * @param callback Function that takes chainId number as an argument
 */
export const onChainChanged = (callback: (chainId: number) => void) => {
  if (isMetaMask) {
    onMounted(() => {
      window.ethereum.on('chainChanged', callback)
    })
    onUnmounted(() => {
      window.ethereum.removeListener('chainChanged', callback)
    })
  }
}
export const initWeb3 = () => {
  return new Promise<void>((resolve, reject) => {
    if (window.ethereum) {
      window.web3 = new Web3(window.ethereum);
    } else if (window.web3) {
      window.web3 = new Web3(window.web3.currentProvider);
    } else {
      return reject(alert("Please install MetaMask"));
    }

    try {
      window.localStorage;
    } catch (e) {
      return reject(
        alert("Please allow 3rd party cookies for web3.js 1.0.0")
      );
    }

    window.web3.defaultChain = "goerli";

    window.web3.extend({
      property: "app",
      methods: [
        {
          name: "signTypedData",
          call: "eth_signTypedData",
          params: 2,
        },
      ],
    });

    resolve();
  });
}
const signTypedData = (address: string, value: string) => {
  console.trace()
  return window.web3.app.signTypedData(
    [
      {
        type: "string",
        name: "challenge",
        value: value,
      },
    ],
    address
  );
}

export const useMetaMaskWallet = () => ({
  connect,
  getAccounts,
  switchAccounts,
  onAccountsChanged,
  onChainChanged,
  signTypedData,
  isMetaMask,
})

export default useMetaMaskWallet
