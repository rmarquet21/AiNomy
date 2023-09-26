<script lang="ts" setup>
import { useAuthStore } from '~/common/stores/authentication';

const authStore = useAuthStore()
let router = useRouter()

const logout = () => {
  authStore.clearToken()
  router.push("/")
}
//wallet.onAccountsChanged((accounts: string[]) => {
//  if (accounts[0]) {
//    console.log('user connected')
//  }
//  else {
//    console.log('wallet address null, user disconected')
//    address.value = null
//  }
//  console.log('account changed to: ', accounts[0])
//})
//wallet.onChainChanged((chainId: number) => {
//  console.log('chain changed to:', chainId)
//})

//const switchAccount = async () => {
//  await wallet.switchAccounts()
//  connect()
//}

//const isConnected = async () => {
//  const accounts = await wallet.getAccounts()
//  if (typeof accounts === 'string')
//    return false
//  return accounts.length > 0
//}
</script>

<template>
  <section class="py-3 px-6 border-b border-gray-300 border-opacity-25">
    <nav class="relative">
      <div class="flex items-center">
        <div class="hidden lg:flex items-center mr-auto font-semibold text-blue-700">
          Ainomy dashboard
        </div>
        <div class="flex w-full justify-end lg:hidden">
          <button class="flex items-center">
            <svg class="block h-4 w-4" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
              <title>Mobile menu</title>
              <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
            </svg>
          </button>
        </div>
        <div class="hidden lg:block cursor-default">
          <ConnectWalletButton
            :address="authStore.address!"
            :txn-count="0"
            :dark="false"
          />
        </div>
        <button class="p-2 bg-red-400 text-white rounded-md ml-2" @click="logout">
          <Carbon:exit />
        </button>
      </div>
    </nav>
  </section>
</template>
