<script setup lang="ts">
import { Buffer } from 'buffer'
import { useMetaMaskWallet } from '../composables/useMetaMaskWallet'
import { generateChallenge, getAuthorization } from '../../../api/client'
import { useAuthStore } from '../stores/authentication'
import { isDark } from '~/common/composables'

const isOpen = ref(false)
const authStore = useAuthStore()
const address = ref('')
const wallet = useMetaMaskWallet()
const router = useRouter()

nextTick(() => {
  if (authStore.address)
    address.value = authStore.address
})

const logout = () => {
  authStore.clearToken()
  address.value = ''
}

const connect = async () => {
  const accounts = await wallet.connect()
  if (typeof accounts === 'string') {
    console.log(`An error occurred${accounts}`)
    return
  }
  try {
    // get challenge
    const nonce: any = await generateChallenge(accounts[0])
    const buff = Buffer.from(nonce, 'utf-8')
    const signature = await window.ethereum.request({
      method: 'personal_sign',
      params: [buff.toString('hex'), accounts[0]],
    })
    const token: any = await getAuthorization(accounts[0], signature)
    authStore.setUser(token, accounts[0])
    router.push('/analysis')
  }
  catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  isDark.value = false
})
</script>

<template>
  <div>
    <section class="xl:bg-contain bg-top bg-no-repeat h-screen">
      <div class="container px-4 mx-auto">
        <nav class="flex fixed w-full h-16 bg-white top-0 left-0 z-10 p-4 border-b border-black-500/50 justify-between items-center py-6">
          <a class="text-3xl font-semibold leading-none" href="#">
            <img class="h-24 w-24" src="/assets/logos/ainomy-blue.svg" alt="" width="auto">
          </a>
          <div class="lg:hidden">
            <button class="navbar-burger flex items-center py-2 px-3 text-blue-600 hover:text-blue-700 rounded border border-blue-200 hover:border-blue-300" @click="isOpen = true">
              <svg class="fill-current h-4 w-4" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <title>Mobile menu</title>
                <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
              </svg>
            </button>
          </div>
          <ul class="hidden lg:flex lg:items-center lg:w-auto lg:space-x-12">
            <li><a class="text-sm text-gray-400 hover:text-gray-500" href="#">Home</a></li>
            <li><a class="text-sm text-gray-400 hover:text-gray-500" href="#increase">Increase AI</a></li>
            <li><a class="text-sm text-gray-400 hover:text-gray-500" href="#about">About ainomy</a></li>
            <li><a class="text-sm text-gray-400 hover:text-gray-500" href="#snews">Newsletter</a></li>
          </ul>
          <div class="hidden lg:flex">
            <ConnectWalletButton
              :address="address"
              :txn-count="0"
              :dark="false"
              @click.stop="connect"
            />
            <button v-if="authStore.token" class="p-2 bg-red-400 text-white rounded-md ml-2" @click="logout">
              <Carbon:exit />
            </button>
          </div>
        </nav>
        <div class="py-12 text-center mt-4">
          <div class="max-w-lg mx-auto mt-10">
            <h2 class="text-3xl md:text-4xl mb-4 font-bold font-heading">
              <span>Revolutionize </span>
              <span class="text-blue-600">medical analysis</span>
              <span> with Ainomy's AI-powered platform</span>
            </h2>
            <p class="text-gray-400 leading-relaxed my-5">
              Powered by advanced AI for accurate and efficient medical analysis.
            </p>
          </div>
          <div>
            <a class="block sm:inline-block py-4 px-8 mb-4 sm:mb-0 sm:mr-3 text-xs text-white text-center font-semibold leading-none bg-blue-600 hover:bg-blue-700 rounded" href="#">Check Now</a><a class="block sm:inline-block py-4 px-8 text-xs text-gray-500 hover:text-gray-600 text-center font-semibold leading-none bg-gray-100 rounded" href="#">Documentation</a>
          </div>
        </div>
        <div class="relative max-w-3xl mt-6 mb-8 mx-auto">
          <img src="/assets/img/pattern-small.png" alt="">
          <div class="absolute" style="top: 3%; left: 9%; width: 82%; height: 90%;">
            <img class="object-contain w-full h-full" src="/assets/img/app-mockup.png" alt="">
          </div>
        </div>
        <div class="flex flex-wrap items-center justify-center max-w-4xl mx-auto pt-8 pb-12">
          <div class="w-1/2 md:w-1/3 lg:w-1/5 px-3 mb-8">
            <img class="mx-auto" src="/assets/logos/nvidia.svg" alt="">
          </div>
          <div class="w-1/2 md:w-1/3 lg:w-1/5 px-3 mb-8">
            <img class="mx-auto" src="/assets/logos/huawei.svg" alt="">
          </div>
        </div>
      </div>
      <div class="navbar-menu fixed top-0 left-0 bottom-0 w-5/6 max-w-sm z-50" :class="isOpen ? '' : 'hidden'">
        <div class="navbar-backdrop fixed inset-0 bg-gray-800 opacity-25" />
        <nav class="relative flex flex-col py-6 px-6 w-full h-full bg-white border-r overflow-y-auto">
          <div class="flex items-center mb-8">
            <a class="mr-auto text-3xl font-semibold leading-none" href="#">
              <img class="h-16" src="/assets/logos/ainomy-blue.svg" alt="" width="auto">
            </a>
            <button class="navbar-close" @click="isOpen = false">
              <svg class="h-6 w-6 text-gray-400 cursor-pointer hover:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewbox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div>
            <ul>
              <li class="mb-1">
                <a class="block p-4 text-sm text-gray-500 hover:bg-blue-50 hover:text-blue-600" href="#">Product</a>
              </li>
              <li class="mb-1">
                <a class="block p-4 text-sm text-gray-500 hover:bg-blue-50 hover:text-blue-600" href="#">Company</a>
              </li>
              <li class="mb-1">
                <a class="block p-4 text-sm text-gray-500 hover:bg-blue-50 hover:text-blue-600" href="#">About Us</a>
              </li>
              <li class="mb-1">
                <a class="block p-4 text-sm text-gray-500 hover:bg-blue-50 hover:text-blue-600" href="#">Features</a>
              </li>
            </ul>
            <div class="mt-4 pt-6 border-t border-gray-100">
              <a class="block px-4 py-3 mb-3 text-xs text-center font-semibold leading-none bg-blue-600 hover:bg-blue-700 text-white rounded" href="#">Sign Up</a><a class="block px-4 py-3 mb-2 text-xs text-center text-blue-600 hover:text-blue-700 font-semibold leading-none border border-blue-200 hover:border-blue-300 rounded" href="#">Log In</a>
            </div>
          </div>
          <div class="mt-auto">
            <p class="my-4 text-xs text-gray-400 space-x-1">
              <span>Get in Touch</span>
              <a class="text-blue-600 hover:text-blue-600 underline" href="#">info@ainomy.eu</a>
            </p>
            <a class="inline-block px-1" href="#">
              <img src="/assets/icons/facebook-blue.svg" alt="">
            </a>
            <a class="inline-block px-1" href="#">
              <img src="/assets/icons/twitter-blue.svg" alt="">
            </a>
            <a class="inline-block px-1" href="#">
              <img src="/assets/icons/instagram-blue.svg" alt="">
            </a>
          </div>
        </nav>
      </div>
    </section>

    <section id="increase" class="pt-20 pb-24 bg-blue-600">
      <div class="max-w-xl mx-auto text-center">
        <span class="inline-block py-1 px-3 bg-blue-500 text-xs text-white font-semibold rounded-xl">Healthcare professional ?</span>
        <h2 class="mt-3 text-3xl md:text-4xl text-white font-bold font-heading">
          help us improve our AI by validating the data in our dataset !
        </h2>
        <div class="mt-6">
          <a class="inline-block text-xs py-4 px-8 bg-white hover:bg-blue-600 text-blue-600 hover:text-white font-semibold leading-none border hover:border-white rounded transition duration-300" href="#">Check Now</a>
        </div>
      </div>
    </section>

    <section id="about" class="py-20">
      <div class="container px-4 mx-auto">
        <div class="flex flex-wrap -mx-8">
          <div class="w-full lg:w-1/2 px-8 h-">
            <div class="mb-12 lg:mb-0 pb-12 lg:pb-0 border-b lg:border-b-0">
              <h2 class="mb-4 text-3xl lg:text-4xl font-bold font-heading">
                Transform the way medical professionals detect and diagnose diseases with Ainomy's powerful AI platform.
              </h2>
              <p class="mb-8 leading-loose text-gray-400">
                Ainomy's platform leverages the latest advances in AI to help medical professionals streamline their analysis process and quickly identify potential anomalies and diseases. With secure blockchain technology and a unique token-based system, our platform ensures the privacy and security of patient data while allowing medical professionals to collaborate more effectively than ever before. By empowering doctors, nurses, and researchers with AI-powered insights, Ainomy is poised to revolutionize the way we approach healthcare.
              </p>
              <a class="inline-block text-xs py-4 px-8 text-white font-semibold leading-none bg-blue-600 hover:bg-blue-700 rounded" href="#">Learn More</a>
            </div>
          </div>
          <div class="w-full lg:w-1/2 px-8">
            <ul class="space-y-12">
              <li class="flex -mx-4">
                <div class="px-4">
                  <span class="flex w-16 h-16 mx-auto items-center justify-center text-2xl font-bold font-heading rounded-full bg-blue-50 text-blue-600">1</span>
                </div>
                <div class="px-4">
                  <h3 class="my-4 text-xl font-semibold">
                    Secure Authentication with Metamask
                  </h3>
                  <p class="text-gray-400 leading-loose">
                    Metamask provides secure authentication for Ainomy's platform, ensuring that only authorized medical professionals can access sensitive patient data.
                  </p>
                </div>
              </li>
              <li class="flex -mx-4">
                <div class="px-4">
                  <span class="flex w-16 h-16 mx-auto items-center justify-center text-2xl font-bold font-heading rounded-full bg-blue-50 text-blue-600">2</span>
                </div>
                <div class="px-4">
                  <h3 class="my-4 text-xl font-semibold">
                    Drag and Drop File Upload
                  </h3>
                  <p class="text-gray-400 leading-loose">
                    Uploading files to Ainomy's platform is simple and streamlined - just drag and drop your files into the designated area.
                  </p>
                </div>
              </li>
              <li class="flex -mx-4">
                <div class="px-4">
                  <span class="flex w-16 h-16 mx-auto items-center justify-center text-2xl font-bold font-heading rounded-full bg-blue-50 text-blue-600">3</span>
                </div>
                <div class="px-4">
                  <h3 class="my-4 text-xl font-semibold">
                    Instant AI-Powered Analysis
                  </h3>
                  <p class="text-gray-400 leading-loose">
                    Ainomy's powerful AI algorithm instantly analyzes the uploaded data to help with diagnosis and treatment planning.
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <section id="news" class="py-20 bg-gray-100">
      <div class="container px-4 mx-auto">
        <div class="px-8 py-20 bg-white rounded shadow">
          <div class="max-w-xl mx-auto text-center">
            <h2 class="mb-4 text-3xl lg:text-4xl font-bold font-heading">
              <span>Join our </span>
              <span class="text-blue-600">Newsletter</span>
              <span> for the latest updates</span>
            </h2>
            <p class="mb-6 text-gray-400">
              Stay up-to-date on the latest developments and insights from Ainomy's AI-powered medical analysis platform. Sign up for our newsletter today.
            </p>
            <div class="flex flex-wrap max-w-lg mx-auto">
              <div class="flex w-full md:w-2/3 px-3 mb-3 md:mb-0 md:mr-6 bg-gray-100 rounded">
                <svg class="h-6 w-6 my-auto text-gray-500" xmlns="http://www.w3.org/2000/svg" viewbox="0 0 20 20" fill="currentColor">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                <input class="w-full pl-3 py-4 text-xs text-gray-400 font-semibold leading-none bg-gray-100 outline-none" type="text" placeholder="Type your e-mail">
              </div>
              <button class="w-full md:w-auto py-4 px-8 text-xs text-white font-semibold leading-none bg-blue-600 hover:bg-blue-700 rounded" type="submit">
                send
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-8">
      <div class="container mx-auto">
        <div class="flex flex-col lg:flex-row mb-5">
          <a class="inline-block lg:mr-auto text-3xl font-semibold leading-none" href="#">
            <img class="h-15 w-30" src="/assets/logos/ainomy-blue.svg" alt="" width="auto">
          </a>
          <ul class="flex lg:flex-row items-center justify-center space-x-12">
            <li><a class="text-lg font-bold font-heading hover:text-gray-600" href="#">Team</a></li>
            <li><a class="text-lg font-bold font-heading hover:text-gray-600" href="#">Contact</a></li>
            <li><a class="text-lg font-bold font-heading hover:text-gray-600" href="#">Blog</a></li>
            <li><a class="text-lg font-bold font-heading hover:text-gray-600" href="#">Pricing</a></li>
          </ul>
        </div>
        <div class="flex flex-col lg:flex-row items-center lg:justify-between">
          <p class="text-xs text-gray-400">
            © {{ new Date().getFullYear() }}. All rights reserved.
          </p>
          <div class="order-first lg:order-last -mx-2 mb-4 lg:mb-0">
            <a class="inline-block px-2" href="https://www.facebook.com/profile.php?id=100091450927792" target="_blank">
              <img src="/assets/icons/facebook-blue.svg" alt="">
            </a>
            <a class="inline-block px-2" href="https://twitter.com/AinomyTech" target="_blank">
              <img src="/assets/icons/twitter-blue.svg" alt="">
            </a>
            <a class="inline-block px-2" href="https://www.instagram.com/ainomytech/" target="_blank">
              <img src="/assets/icons/instagram-blue.svg" alt="">
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
