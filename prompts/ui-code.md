<!-- Login Screen -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Login - SecureEdit AI</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">tailwind.config = {darkMode: "class", theme: {extend: {colors: {primary: "#39E079", "background-light": "#f6f8f7", "background-dark": "#122017"}, fontFamily: {display: "Inter"}, borderRadius: {DEFAULT: "0.25rem", lg: "0.5rem", xl: "0.75rem", full: "9999px"}}}};</script>
<style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark min-h-screen flex flex-col font-display">
<!-- Top Navigation -->
<header class="flex items-center justify-between border-b border-gray-200 dark:border-[#282e39] px-6 py-4 md:px-10">
<div class="flex items-center gap-3 text-gray-900 dark:text-white">
<div class="size-8 text-primary">
<svg fill="currentColor" viewbox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
<path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z"></path>
</svg>
</div>
<h2 class="text-lg font-bold leading-tight tracking-tight">SecureEdit AI</h2>
</div>
<div class="flex items-center gap-4">
<span class="text-sm text-gray-600 dark:text-[#9da6b9] hidden sm:block">Don't have an account?</span>
<button class="flex cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-gray-200 dark:bg-[#282e39] text-gray-900 dark:text-white text-sm font-medium leading-normal hover:bg-gray-300 dark:hover:bg-[#3b4354] transition-colors">
<span class="truncate">Sign Up</span>
</button>
</div>
</header>
<!-- Main Content -->
<main class="flex-1 flex flex-col items-center justify-center p-4 md:p-10 relative overflow-hidden">
<!-- Abstract Background Decoration -->
<div class="absolute inset-0 z-0 pointer-events-none opacity-20 dark:opacity-10">
<div class="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-primary rounded-full blur-[150px]"></div>
<div class="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-purple-600 rounded-full blur-[150px]"></div>
</div>
<div class="layout-content-container flex flex-col md:flex-row max-w-[1000px] w-full flex-1 gap-8 z-10">
<!-- Left Column: Login Form -->
<div class="flex flex-col justify-center flex-1 max-w-[480px] w-full mx-auto md:mx-0">
<div class="flex flex-col gap-6 p-2">
<div class="flex flex-col gap-2">
<h1 class="text-gray-900 dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">Welcome back</h1>
<p class="text-gray-600 dark:text-[#9da6b9] text-base font-normal leading-normal">Log in to access your secure workspace.</p>
</div>
<form action="#" class="flex flex-col gap-5 mt-4">
<!-- Email Field -->
<label class="flex flex-col w-full gap-2">
<span class="text-gray-900 dark:text-white text-sm font-medium leading-normal">Email Address</span>
<div class="relative">
<span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 material-symbols-outlined">mail</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4354] bg-white dark:bg-[#1c1f27] focus:border-primary h-12 pl-12 placeholder:text-gray-400 dark:placeholder:text-[#9da6b9] pr-4 text-base font-normal leading-normal transition-all" placeholder="name@company.com" required="" type="email"/>
</div>
</label>
<!-- Password Field -->
<label class="flex flex-col w-full gap-2">
<div class="flex justify-between items-center">
<span class="text-gray-900 dark:text-white text-sm font-medium leading-normal">Password</span>
<a class="text-sm font-medium text-primary hover:text-primary/80 transition-colors" href="#">Forgot password?</a>
</div>
<div class="relative w-full rounded-lg">
<span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 material-symbols-outlined">lock</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-gray-900 dark:text-white focus:outline-0 focus:ring-2 focus:ring-primary/50 border border-gray-300 dark:border-[#3b4354] bg-white dark:bg-[#1c1f27] focus:border-primary h-12 pl-12 pr-12 placeholder:text-gray-400 dark:placeholder:text-[#9da6b9] text-base font-normal leading-normal transition-all" placeholder="Enter your password" required="" type="password"/>
<button class="absolute right-0 top-0 h-12 w-12 flex items-center justify-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors" type="button">
<span class="material-symbols-outlined text-[20px]">visibility</span>
</button>
</div>
</label>
<!-- Action Button -->
<button class="flex w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-4 bg-primary text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-blue-600 transition-colors shadow-lg shadow-primary/20 mt-2" type="submit">
<span class="truncate">Log In</span>
</button>
<!-- Divider -->
<div class="relative flex py-2 items-center">
<div class="flex-grow border-t border-gray-300 dark:border-[#3b4354]"></div>
<span class="flex-shrink-0 mx-4 text-gray-400 text-xs uppercase tracking-wider">Or continue with</span>
<div class="flex-grow border-t border-gray-300 dark:border-[#3b4354]"></div>
</div>
<!-- Social Login -->
<div class="grid grid-cols-2 gap-4">
<button class="flex items-center justify-center gap-2 h-11 rounded-lg border border-gray-300 dark:border-[#3b4354] bg-white dark:bg-[#1c1f27] hover:bg-gray-50 dark:hover:bg-[#282e39] transition-colors text-gray-900 dark:text-white font-medium text-sm" type="button">
<svg class="w-5 h-5" viewbox="0 0 24 24">
<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"></path>
<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"></path>
<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.26.81-.58z" fill="#FBBC05"></path>
<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"></path>
</svg>
                                Google
                            </button>
<button class="flex items-center justify-center gap-2 h-11 rounded-lg border border-gray-300 dark:border-[#3b4354] bg-white dark:bg-[#1c1f27] hover:bg-gray-50 dark:hover:bg-[#282e39] transition-colors text-gray-900 dark:text-white font-medium text-sm" type="button">
<svg class="w-5 h-5 text-gray-900 dark:text-white" fill="currentColor" viewbox="0 0 24 24">
<path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.1 1.88-2.5 5.75.1 6.74-.24.75-.59 1.54-.98 2.27-.67 1.25-1.36 2.5-2.17 2.2zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"></path>
</svg>
                                Apple
                            </button>
</div>
</form>
<div class="flex items-center justify-center gap-2 mt-4 opacity-70">
<span class="material-symbols-outlined text-green-500 text-sm">lock</span>
<p class="text-xs text-gray-500 dark:text-[#9da6b9]">End-to-end encrypted &amp; Secure</p>
</div>
</div>
</div>
<!-- Right Column: Visual (Hidden on mobile) -->
<div class="hidden md:flex flex-1 items-center justify-center">
<div class="w-full h-full max-h-[600px] bg-gray-900/50 rounded-xl border border-gray-800 backdrop-blur-sm relative overflow-hidden group">
<!-- Image Container -->
<div class="w-full h-full bg-center bg-cover absolute inset-0 opacity-60 mix-blend-overlay" data-alt="Abstract dark blue and purple waveform visualization representing AI processing" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuCDac5RFCVIATlbfFcG1Wfd5GG6mN3IG1GI6YhrG7m40QAKjfuPrfTxY2nVXyCwF-XqOlICe7kbqWI4dSC7qLnCU1YUCVZo-E26ZCPXrwFr-swkttXyeUcGtstOVzQDyJwB2KrWWvXbAVC1MNg805GgqLmyJVYbD-fH5HhoOf-G1rvI4YybXvB3NWWVpITPrxUfL1Qi71HgYAjVJicUFfsLHAVUkeX9DihjQ97Q4agwHraJn0rv1r810njKSIcP9S4nxT8dZW_ULBi_");'>
</div>
<!-- Overlay content on the visual -->
<div class="absolute inset-0 flex flex-col justify-end p-8 bg-gradient-to-t from-background-dark via-background-dark/50 to-transparent">
<div class="flex items-center gap-2 mb-2">
<span class="inline-flex items-center rounded-full bg-primary/20 px-2.5 py-0.5 text-xs font-medium text-blue-200">
                                New v2.0
                           </span>
</div>
<h3 class="text-white text-2xl font-bold mb-2">AI-Powered Privacy</h3>
<p class="text-gray-400 text-sm max-w-sm">
                            Our advanced algorithms automatically detect and redact sensitive information in your video footage before it even leaves your device.
                        </p>
</div>
</div>
</div>
</div>
</main>
</body></html>

<!-- Registration Screen -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Registration - PrivacyEdit AI</title>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">tailwind.config = {darkMode: "class", theme: {extend: {colors: {primary: "#39E079", "background-light": "#f6f8f7", "background-dark": "#122017", "card-dark": "#111318", "input-dark": "#1c1f27", "border-dark": "#3b4354", "text-muted": "#9da6b9"}, fontFamily: {display: "Inter"}, borderRadius: {DEFAULT: "0.25rem", lg: "0.5rem", xl: "0.75rem", full: "9999px"}}}};</script>
<style>
        /* Custom scrollbar for clean look */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #101622;
        }
        ::-webkit-scrollbar-thumb {
            background: #282e39;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #3b4354;
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-white min-h-screen flex flex-col relative overflow-x-hidden selection:bg-primary/30 selection:text-white">
<!-- Decorative Background Elements -->
<div class="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
<!-- Abstract gradient orb top left -->
<div class="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] bg-primary/10 rounded-full blur-[100px] opacity-60"></div>
<!-- Abstract gradient orb bottom right -->
<div class="absolute bottom-[-10%] right-[-10%] w-[30rem] h-[30rem] bg-purple-500/10 rounded-full blur-[100px] opacity-40"></div>
</div>
<div class="relative z-10 flex-1 flex flex-col justify-center items-center p-4 sm:p-6 lg:p-8">
<!-- Main Card Container -->
<div class="w-full max-w-[500px] flex flex-col gap-6">
<!-- Logo Header -->
<div class="flex items-center justify-center gap-3 mb-2">
<div class="size-8 text-primary">
<svg fill="none" viewbox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
<path d="M13.8261 17.4264C16.7203 18.1174 20.2244 18.5217 24 18.5217C27.7756 18.5217 31.2797 18.1174 34.1739 17.4264C36.9144 16.7722 39.9967 15.2331 41.3563 14.1648L24.8486 40.6391C24.4571 41.267 23.5429 41.267 23.1514 40.6391L6.64374 14.1648C8.00331 15.2331 11.0856 16.7722 13.8261 17.4264Z" fill="currentColor"></path>
<path clip-rule="evenodd" d="M39.998 12.236C39.9944 12.2537 39.9875 12.2845 39.9748 12.3294C39.9436 12.4399 39.8949 12.5741 39.8346 12.7175C39.8168 12.7597 39.7989 12.8007 39.7813 12.8398C38.5103 13.7113 35.9788 14.9393 33.7095 15.4811C30.9875 16.131 27.6413 16.5217 24 16.5217C20.3587 16.5217 17.0125 16.131 14.2905 15.4811C12.0012 14.9346 9.44505 13.6897 8.18538 12.8168C8.17384 12.7925 8.16216 12.767 8.15052 12.7408C8.09919 12.6249 8.05721 12.5114 8.02977 12.411C8.00356 12.3152 8.00039 12.2667 8.00004 12.2612C8.00004 12.261 8 12.2607 8.00004 12.2612C8.00004 12.2359 8.0104 11.9233 8.68485 11.3686C9.34546 10.8254 10.4222 10.2469 11.9291 9.72276C14.9242 8.68098 19.1919 8 24 8C28.8081 8 33.0758 8.68098 36.0709 9.72276C37.5778 10.2469 38.6545 10.8254 39.3151 11.3686C39.9006 11.8501 39.9857 12.1489 39.998 12.236ZM4.95178 15.2312L21.4543 41.6973C22.6288 43.5809 25.3712 43.5809 26.5457 41.6973L43.0534 15.223C43.0709 15.1948 43.0878 15.1662 43.104 15.1371L41.3563 14.1648C43.104 15.1371 43.1038 15.1374 43.104 15.1371L43.1051 15.135L43.1065 15.1325L43.1101 15.1261L43.1199 15.1082C43.1276 15.094 43.1377 15.0754 43.1497 15.0527C43.1738 15.0075 43.2062 14.9455 43.244 14.8701C43.319 14.7208 43.4196 14.511 43.5217 14.2683C43.6901 13.8679 44 13.0689 44 12.2609C44 10.5573 43.003 9.22254 41.8558 8.2791C40.6947 7.32427 39.1354 6.55361 37.385 5.94477C33.8654 4.72057 29.133 4 24 4C18.867 4 14.1346 4.72057 10.615 5.94478C8.86463 6.55361 7.30529 7.32428 6.14419 8.27911C4.99695 9.22255 3.99999 10.5573 3.99999 12.2609C3.99999 13.1275 4.29264 13.9078 4.49321 14.3607C4.60375 14.6102 4.71348 14.8196 4.79687 14.9689C4.83898 15.0444 4.87547 15.1065 4.9035 15.1529C4.91754 15.1762 4.92954 15.1957 4.93916 15.2111L4.94662 15.223L4.95178 15.2312ZM35.9868 18.996L24 38.22L12.0131 18.996C12.4661 19.1391 12.9179 19.2658 13.3617 19.3718C16.4281 20.1039 20.0901 20.5217 24 20.5217C27.9099 20.5217 31.5719 20.1039 34.6383 19.3718C35.082 19.2658 35.5339 19.1391 35.9868 18.996Z" fill="currentColor" fill-rule="evenodd"></path>
</svg>
</div>
<h2 class="text-white text-xl font-bold leading-tight tracking-[-0.015em]">PrivacyEdit AI</h2>
</div>
<!-- Card -->
<div class="bg-card-dark border border-[#282e39] shadow-2xl rounded-2xl p-6 sm:p-10 backdrop-blur-sm">
<!-- Heading Group -->
<div class="flex flex-col gap-2 mb-8 text-center">
<h1 class="text-white text-3xl font-black leading-tight tracking-[-0.033em]">Start Creating Securely</h1>
<p class="text-text-muted text-base font-normal leading-normal">AI-powered video editing with zero data compromise.</p>
</div>
<!-- Registration Form -->
<form action="#" class="flex flex-col gap-5">
<!-- Full Name -->
<label class="flex flex-col gap-2">
<span class="text-white text-sm font-medium leading-normal">Full Name</span>
<div class="relative group">
<span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors text-[20px]">person</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary border border-border-dark bg-input-dark h-12 placeholder:text-text-muted pl-[44px] pr-[15px] text-sm font-normal leading-normal transition-all" placeholder="Enter your full name" type="text"/>
</div>
</label>
<!-- Work Email -->
<label class="flex flex-col gap-2">
<span class="text-white text-sm font-medium leading-normal">Work Email</span>
<div class="relative group">
<span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors text-[20px]">mail</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary border border-border-dark bg-input-dark h-12 placeholder:text-text-muted pl-[44px] pr-[15px] text-sm font-normal leading-normal transition-all" placeholder="name@company.com" type="email"/>
</div>
</label>
<!-- Password Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
<label class="flex flex-col gap-2">
<span class="text-white text-sm font-medium leading-normal">Password</span>
<div class="relative group">
<span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors text-[20px]">lock</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary border border-border-dark bg-input-dark h-12 placeholder:text-text-muted pl-[44px] pr-[15px] text-sm font-normal leading-normal transition-all" placeholder="Min. 8 characters" type="password"/>
</div>
</label>
<label class="flex flex-col gap-2">
<span class="text-white text-sm font-medium leading-normal">Confirm Password</span>
<div class="relative group">
<span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors text-[20px]">lock_reset</span>
<input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-white focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary border border-border-dark bg-input-dark h-12 placeholder:text-text-muted pl-[44px] pr-[15px] text-sm font-normal leading-normal transition-all" placeholder="Re-enter password" type="password"/>
</div>
</label>
</div>
<!-- Terms Checkbox -->
<div class="flex items-start gap-3 mt-1">
<div class="flex h-5 items-center">
<input class="h-4 w-4 rounded border-border-dark bg-input-dark text-primary focus:ring-primary focus:ring-offset-card-dark focus:ring-offset-1" id="terms" type="checkbox"/>
</div>
<div class="text-sm leading-5">
<label class="font-normal text-text-muted" for="terms">
                                I agree to the <a class="font-medium text-white hover:underline decoration-primary decoration-2 underline-offset-4" href="#">Terms and Conditions</a> and <a class="font-medium text-white hover:underline decoration-primary decoration-2 underline-offset-4" href="#">Privacy Policy</a>.
                            </label>
</div>
</div>
<!-- Register Button -->
<button class="flex w-full cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-4 bg-primary hover:bg-primary/90 transition-colors text-white text-base font-bold leading-normal tracking-[0.015em] shadow-lg shadow-primary/20 mt-2 group">
<span class="truncate mr-2">Create Account</span>
<span class="material-symbols-outlined text-[20px] transition-transform group-hover:translate-x-1">arrow_forward</span>
</button>
<!-- Divider -->
<div class="relative flex py-2 items-center">
<div class="flex-grow border-t border-border-dark"></div>
<span class="flex-shrink-0 mx-4 text-text-muted text-xs uppercase tracking-wider">Or register with</span>
<div class="flex-grow border-t border-border-dark"></div>
</div>
<!-- Social Login -->
<div class="grid grid-cols-2 gap-4">
<button class="flex items-center justify-center gap-2 h-10 rounded-lg border border-border-dark bg-input-dark hover:bg-[#282e39] transition-colors text-white text-sm font-medium" type="button">
<img alt="Google logo" class="w-5 h-5" data-alt="Google G Logo" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCJjyXUpYtR2L-K-uUdQgfcFd-sIiAhYzi80CzI0AS7tBiUxygCcJXW50pKya96nvfg1Vw9FpU_P15ILEnmTky6RwBjIpjzlrdT26UduHClJUc2O8P3tTUzOdwuetSOCPlr7xHyg-JwTxYpzCqKiQ6eV8wVcpExNeTl7bLhqJxu7456YvmGfbrk_6TjHPnIUmCJMOVv4BG9ZX1sl-AETlMTl8kHnLf1BwcOzo-qo2I_E2SCeS3xP_X1eCDiUwFQAx9C-4wDPty7KzS2"/>
                            Google
                        </button>
<button class="flex items-center justify-center gap-2 h-10 rounded-lg border border-border-dark bg-input-dark hover:bg-[#282e39] transition-colors text-white text-sm font-medium" type="button">
<img alt="GitHub logo" class="w-5 h-5 invert" data-alt="GitHub Octocat Logo" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC_rJAnLbDxjAC-Ksyi6UPf2WFsBcs7MRVjU2M-7Z1h-9X-yiMyAIvCDSmh5bFeaVQwXO_t7e0DOPV8bc6lDQfmGUEwXx3u-_0kKqvmpB4FBPUAjJKZfzNHpbT17_SLmpMbOapuepUaonKL-vY-q8cjyvklgh6V9TD061lBa37mvMD0ycro9n-4bHZhovgElCgt7eyR7JBtsgGYE2eAOFLdreT1kem1kXQeTRcEQ7UpwWsgR7uOIuorhKa-ZKWMWebV17sqIqMrV7u-"/>
                            GitHub
                        </button>
</div>
</form>
<!-- Footer Link -->
<div class="mt-8 text-center">
<p class="text-text-muted text-sm font-normal">
                        Already have an account? 
                        <a class="text-primary hover:text-white transition-colors font-semibold ml-1" href="#">Log In</a>
</p>
</div>
<!-- Trust Badge -->
<div class="mt-8 flex justify-center">
<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20 text-green-400 text-xs font-medium">
<span class="material-symbols-outlined text-[14px]">lock</span>
                        End-to-end encrypted
                    </div>
</div>
</div>
<!-- Bottom Links -->
<div class="flex justify-center gap-6 text-xs text-text-muted/60">
<a class="hover:text-text-muted transition-colors" href="#">Help Center</a>
<a class="hover:text-text-muted transition-colors" href="#">Privacy</a>
<a class="hover:text-text-muted transition-colors" href="#">Terms</a>
</div>
</div>
</div>
</body></html>

<!-- Dashboard Screen -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PrivacyEdit AI Dashboard</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script id="tailwind-config">tailwind.config = {darkMode: "class", theme: {extend: {colors: {primary: "#39E079", "background-light": "#f6f8f7", "background-dark": "#122017", "card-dark": "#181b21", "border-dark": "#282e39"}, fontFamily: {display: "Inter"}, borderRadius: {DEFAULT: "0.25rem", lg: "0.5rem", xl: "0.75rem", full: "9999px"}}}};</script>
<style>
        /* Custom scrollbar for dark mode webkit */
        .dark ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        .dark ::-webkit-scrollbar-track {
            background: #101622; 
        }
        .dark ::-webkit-scrollbar-thumb {
            background: #282e39; 
            border-radius: 4px;
        }
        .dark ::-webkit-scrollbar-thumb:hover {
            background: #374151; 
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display antialiased overflow-hidden">
<div class="flex h-screen w-full">
<!-- Sidebar -->
<aside class="hidden w-64 flex-col justify-between border-r border-slate-200 dark:border-border-dark bg-white dark:bg-background-dark p-4 md:flex">
<div class="flex flex-col gap-6">
<!-- Logo -->
<div class="flex items-center gap-3 px-2">
<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white">
<span class="material-symbols-outlined text-2xl">security</span>
</div>
<h1 class="text-xl font-bold tracking-tight text-slate-900 dark:text-white">PrivacyEdit AI</h1>
</div>
<!-- Navigation -->
<nav class="flex flex-col gap-2">
<a class="flex items-center gap-3 rounded-lg bg-primary/10 px-3 py-2.5 text-primary dark:bg-primary dark:text-white transition-colors" href="#">
<span class="material-symbols-outlined filled">dashboard</span>
<span class="font-medium">Dashboard</span>
</a>
<a class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-card-dark dark:hover:text-white transition-colors" href="#">
<span class="material-symbols-outlined">folder</span>
<span class="font-medium">Projects</span>
</a>
<a class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-card-dark dark:hover:text-white transition-colors" href="#">
<span class="material-symbols-outlined">auto_fix_high</span>
<span class="font-medium">AI Tools</span>
</a>
<a class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-card-dark dark:hover:text-white transition-colors" href="#">
<span class="material-symbols-outlined">settings</span>
<span class="font-medium">Settings</span>
</a>
</nav>
</div>
<!-- Sidebar Footer -->
<div class="flex flex-col gap-4 px-2">
<div class="flex flex-col gap-2">
<div class="flex items-center justify-between text-xs font-medium text-slate-500 dark:text-slate-400">
<span>Storage</span>
<span>2.5GB / 10GB</span>
</div>
<div class="h-1.5 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-card-dark">
<div class="h-full w-1/4 rounded-full bg-primary"></div>
</div>
</div>
<button class="flex w-full items-center justify-center gap-2 rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-bold text-white transition-colors hover:bg-slate-800 dark:bg-card-dark dark:hover:bg-slate-700">
<span class="material-symbols-outlined text-[18px]">diamond</span>
<span>Upgrade Plan</span>
</button>
</div>
</aside>
<!-- Main Content -->
<main class="flex flex-1 flex-col overflow-y-auto">
<!-- Top Header -->
<header class="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-slate-200 bg-white/80 px-6 backdrop-blur-md dark:border-border-dark dark:bg-background-dark/80">
<div class="flex items-center gap-4 md:hidden">
<button class="text-slate-500 dark:text-white">
<span class="material-symbols-outlined">menu</span>
</button>
<span class="text-lg font-bold text-slate-900 dark:text-white">Dashboard</span>
</div>
<div class="hidden items-center gap-4 md:flex">
<!-- Breadcrumbs or simple title can go here -->
</div>
<!-- Search and Profile -->
<div class="flex w-full items-center justify-end gap-4 md:w-auto">
<div class="relative hidden sm:block">
<span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
<input class="h-10 w-64 rounded-lg border-none bg-slate-100 pl-10 pr-4 text-sm font-medium text-slate-900 placeholder-slate-500 focus:ring-2 focus:ring-primary dark:bg-card-dark dark:text-white dark:placeholder-slate-500" placeholder="Search projects..." type="text"/>
</div>
<div class="flex items-center gap-3">
<button class="flex h-10 w-10 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-card-dark transition-colors">
<span class="material-symbols-outlined">notifications</span>
</button>
<div class="h-10 w-10 overflow-hidden rounded-full border border-slate-200 dark:border-border-dark" data-alt="User profile avatar with blue background">
<img alt="User Avatar" class="h-full w-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDyi-gDVojVG-YQ_407iQHJQfIbpD6bQMjcQZ0hjpRDnt1uJQCLEFH-3hv8eNoNCXzo3EgcNyHo5xh3oFIAPiCRPsqIg32jK1JERHW-V_nSLUUkdWCwfJvmQh1S2esP4jBuUIziB7TUpsRMr9viT2J_Mmx1mmRFZoWF8KcPc39rQT7B3pMg-rPjItZAH_Bt4fdONoXG9QzxTd1YCVFS17jpYHFl_3efPd_mTUCIXWnuA1jMWdZMp6HfF_p5uRk-9o77dQHsSYJIa05A"/>
</div>
</div>
</div>
</header>
<div class="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-8 p-6 lg:p-10">
<!-- Welcome Section -->
<div class="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
<div>
<h2 class="text-3xl font-black tracking-tight text-slate-900 dark:text-white sm:text-4xl">Welcome back, Alex</h2>
<p class="mt-2 text-base text-slate-500 dark:text-slate-400">Ready to create secure content today? All your data is encrypted.</p>
</div>
<button class="group flex items-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-bold text-white shadow-lg shadow-primary/25 transition-all hover:bg-blue-600 active:scale-95">
<span class="material-symbols-outlined">add</span>
<span>New Project</span>
</button>
</div>
<!-- Quick AI Tools -->
<section>
<div class="mb-4 flex items-center justify-between">
<h3 class="text-lg font-bold text-slate-900 dark:text-white">Quick AI Tools</h3>
</div>
<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
<!-- Tool 1 -->
<button class="group flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-all hover:border-primary/50 hover:shadow-md dark:border-border-dark dark:bg-card-dark dark:hover:border-primary/50">
<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 text-primary dark:bg-primary/20 dark:text-primary-400">
<span class="material-symbols-outlined">graphic_eq</span>
</div>
<div>
<h4 class="font-bold text-slate-900 dark:text-white">Remove Silence</h4>
<p class="text-xs text-slate-500 dark:text-slate-400">Automatically cut silent parts</p>
</div>
</button>
<!-- Tool 2 -->
<button class="group flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-all hover:border-primary/50 hover:shadow-md dark:border-border-dark dark:bg-card-dark dark:hover:border-primary/50">
<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400">
<span class="material-symbols-outlined">explicit</span>
</div>
<div>
<h4 class="font-bold text-slate-900 dark:text-white">Word Filter</h4>
<p class="text-xs text-slate-500 dark:text-slate-400">Bleep or cut profanity</p>
</div>
</button>
<!-- Tool 3 -->
<button class="group flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-all hover:border-primary/50 hover:shadow-md dark:border-border-dark dark:bg-card-dark dark:hover:border-primary/50">
<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400">
<span class="material-symbols-outlined">subtitles</span>
</div>
<div>
<h4 class="font-bold text-slate-900 dark:text-white">Auto-Subtitles</h4>
<p class="text-xs text-slate-500 dark:text-slate-400">Generate captions instantly</p>
</div>
</button>
<!-- Tool 4 -->
<button class="group flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-5 text-left shadow-sm transition-all hover:border-primary/50 hover:shadow-md dark:border-border-dark dark:bg-card-dark dark:hover:border-primary/50">
<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-100 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400">
<span class="material-symbols-outlined">auto_videocam</span>
</div>
<div>
<h4 class="font-bold text-slate-900 dark:text-white">AI Shorts</h4>
<p class="text-xs text-slate-500 dark:text-slate-400">Create viral clips from long form</p>
</div>
</button>
</div>
</section>
<!-- Recent Projects -->
<section class="flex flex-col gap-4">
<div class="flex items-center justify-between">
<div class="flex items-center gap-3">
<h3 class="text-lg font-bold text-slate-900 dark:text-white">Recent Projects</h3>
<span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-600 dark:bg-card-dark dark:text-slate-400">8</span>
</div>
<div class="flex items-center gap-2">
<button class="flex items-center gap-1 text-sm font-medium text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white">
<span class="material-symbols-outlined text-[18px]">sort</span>
                                Sort by Date
                            </button>
</div>
</div>
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
<!-- Upload New Card -->
<div class="group relative flex min-h-[260px] flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 p-6 text-center transition-all hover:border-primary hover:bg-blue-50/50 dark:border-border-dark dark:bg-transparent dark:hover:border-primary dark:hover:bg-card-dark/30">
<div class="flex h-14 w-14 items-center justify-center rounded-full bg-slate-200 text-slate-500 transition-colors group-hover:bg-primary group-hover:text-white dark:bg-card-dark dark:text-slate-400">
<span class="material-symbols-outlined text-2xl">upload_file</span>
</div>
<div class="space-y-1">
<h4 class="font-bold text-slate-900 dark:text-white">Upload New Video</h4>
<p class="text-xs text-slate-500 dark:text-slate-400">Drag &amp; drop or click to browse</p>
</div>
<input aria-label="Upload video" class="absolute inset-0 cursor-pointer opacity-0" type="file"/>
</div>
<!-- Project Card 1 -->
<div class="group flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md dark:border-border-dark dark:bg-card-dark">
<div class="relative aspect-video w-full overflow-hidden bg-slate-100 dark:bg-black/50" data-alt="Abstract colorful gradient wave pattern">
<img alt="Abstract gradient background" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDDEShNWpZwlHJ7i5zs_vcxcXcmJmvJQh80dN_9VUi92m9KOwSBVcnzXbeDU24QMKO-TMV5PqD0opL4g8djy1fFL2beqlv3WoIWNkWfkm7kxTbRlR1VowxBLtV-HZMmoogvGqPJhrezbtkYLRLmKJIdHK17HIEhHRHm3-AtpChGGl_nH2tvt2qKqp6OG1i7k8_DQncABT-xkvVRmy1J-Png6db0iATifPQ2ZAIqt36200ZrFbHthUhRg4OnzzqOBJKweWLhyIYHBXUR"/>
<div class="absolute right-2 top-2 rounded-md bg-black/60 px-1.5 py-0.5 text-[10px] font-bold text-white backdrop-blur-sm">
                                    12:34
                                </div>
<div class="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity group-hover:opacity-100 bg-black/30 backdrop-blur-[2px]">
<button class="rounded-full bg-white p-2 text-slate-900 shadow-lg hover:scale-110 transition-transform">
<span class="material-symbols-outlined">edit</span>
</button>
</div>
</div>
<div class="flex flex-1 flex-col justify-between p-4">
<div class="flex items-start justify-between gap-2">
<div>
<h4 class="line-clamp-1 font-bold text-slate-900 dark:text-white">Marketing_Campaign_v2.mp4</h4>
<p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Edited 2h ago</p>
</div>
<button class="text-slate-400 hover:text-slate-600 dark:hover:text-white">
<span class="material-symbols-outlined text-[20px]">more_vert</span>
</button>
</div>
<div class="mt-4 flex items-center gap-2">
<span class="flex h-2 w-2 rounded-full bg-green-500"></span>
<span class="text-xs font-medium text-slate-600 dark:text-slate-300">Ready</span>
</div>
</div>
</div>
<!-- Project Card 2 (Processing) -->
<div class="group flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md dark:border-border-dark dark:bg-card-dark">
<div class="relative aspect-video w-full overflow-hidden bg-slate-100 dark:bg-black/50" data-alt="Tech interview setup with soft lighting">
<img alt="Podcast studio setup" class="h-full w-full object-cover opacity-60" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBjmRnm-vqA6UFY_WoYqFVp6xABj3CAlHCYxKIPDi9-KImv2FgufrvpTw2qY-Hl78tESsaT5JBO9vDq1yZa4qkeuzEgNtgsTLbyyT9-AQ_pkK0Et9Sb7WkzS83WaQHmu_uphFC997ItmMmmlwXNYbbagLw08R5T5XBQQ3U4OI_A55hc-N_rcaZUinZuPpHoSdqDaapus15BpKoTjnpjcdycMI6azSlJinwNVCN5rS-aiifoOYvKUfD7I8JB3gw7K2plQ46-QVBYJnMK"/>
<div class="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-[1px]">
<div class="flex flex-col items-center gap-2">
<div class="h-8 w-8 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
<span class="text-xs font-bold text-white">AI Processing...</span>
</div>
</div>
</div>
<div class="flex flex-1 flex-col justify-between p-4">
<div class="flex items-start justify-between gap-2">
<div>
<h4 class="line-clamp-1 font-bold text-slate-900 dark:text-white">Podcast_Interview_Ep4.mov</h4>
<p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Uploaded 15m ago</p>
</div>
<button class="text-slate-400 hover:text-slate-600 dark:hover:text-white">
<span class="material-symbols-outlined text-[20px]">more_vert</span>
</button>
</div>
<div class="mt-4">
<div class="flex items-center justify-between text-xs font-medium text-primary mb-1.5">
<span>Removing Silence</span>
<span>78%</span>
</div>
<div class="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
<div class="h-full w-[78%] rounded-full bg-primary"></div>
</div>
</div>
</div>
</div>
<!-- Project Card 3 -->
<div class="group flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md dark:border-border-dark dark:bg-card-dark">
<div class="relative aspect-video w-full overflow-hidden bg-slate-100 dark:bg-black/50" data-alt="Gaming setup with neon lights">
<img alt="Gaming monitor setup" class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCRZFnhXwAAduuCclZY8YV2S11ZyqXTWqwqhHlmFsUMTyMIivb43EivqX1vQTxDSrumGYZ7aQ_MESuV_6HISOuORIpXaTko5dKDdCvBC_rFBat3C1caUpzdf25KMDAZDrXzsWmth6KQ6d7E1F9bmhqNOzzSpY-s_5ZnTor3yylB7hahB9B-iHptQgjnW-IJisvCnbqh6JM7MTCDpOY4JI9E_RjZ_N1Rh3pEJ4Cux1cVtTuSsVIKFjBBq6rPiR5OYGpwP_uNIgyyGn9l"/>
<div class="absolute right-2 top-2 rounded-md bg-black/60 px-1.5 py-0.5 text-[10px] font-bold text-white backdrop-blur-sm">
                                    08:45
                                </div>
<div class="absolute inset-0 flex items-center justify-center opacity-0 transition-opacity group-hover:opacity-100 bg-black/30 backdrop-blur-[2px]">
<button class="rounded-full bg-white p-2 text-slate-900 shadow-lg hover:scale-110 transition-transform">
<span class="material-symbols-outlined">edit</span>
</button>
</div>
</div>
<div class="flex flex-1 flex-col justify-between p-4">
<div class="flex items-start justify-between gap-2">
<div>
<h4 class="line-clamp-1 font-bold text-slate-900 dark:text-white">Gameplay_Highlight_Reel.mp4</h4>
<p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Edited yesterday</p>
</div>
<button class="text-slate-400 hover:text-slate-600 dark:hover:text-white">
<span class="material-symbols-outlined text-[20px]">more_vert</span>
</button>
</div>
<div class="mt-4 flex items-center gap-2">
<span class="flex h-2 w-2 rounded-full bg-green-500"></span>
<span class="text-xs font-medium text-slate-600 dark:text-slate-300">Ready</span>
</div>
</div>
</div>
</div>
</section>
<!-- CTA Banner -->
<div class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-primary to-blue-700 p-8 text-white md:p-12">
<div class="absolute right-0 top-0 h-full w-1/2 opacity-10">
<svg class="h-full w-full" preserveaspectratio="none" viewbox="0 0 100 100">
<path d="M0 100 L100 0 L100 100 Z" fill="white"></path>
</svg>
</div>
<div class="relative z-10 flex flex-col items-start gap-4 max-w-2xl">
<div class="flex h-12 w-12 items-center justify-center rounded-xl bg-white/20 backdrop-blur-sm">
<span class="material-symbols-outlined text-3xl">lock</span>
</div>
<h2 class="text-2xl font-bold md:text-3xl">Privacy First Editing</h2>
<p class="text-blue-100 max-w-lg">Your videos are processed in a secure, isolated environment. We never use your content to train our models without your explicit permission.</p>
<button class="mt-2 rounded-lg bg-white px-5 py-2.5 text-sm font-bold text-primary transition-colors hover:bg-blue-50">
                            View Security Report
                        </button>
</div>
</div>
</div>
</main>
</div>
</body></html>

<!-- Landing Page -->
<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>SilentCut AI - Privacy-First Video Editor</title>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
            extend: {
                colors: {
                // Cyberpunk colors
                "primary": "#00FF7F", // Electric Green
                "secondary-accent": "#BF00FF", // Neon Purple for some accents if needed, though primary is dominant
                "background-light": "#0a030f", // Almost pitch-black with subtle indigo/violet
                "background-dark": "#0a030f", // Same for dark mode
                "dark-panel": "#1a0823", // Darker panel background, subtle violet hint
                "dark-border": "#280a3a", // Dark border with violet hint
                "text-primary": "#F0F0F0", // Stark white
                "text-secondary": "#A0A0A0", // Light gray
                "text-muted": "#606060", // Muted gray
                },
                fontFamily: {
                "display": ["Inter", "sans-serif"]
                },
                borderRadius: {"DEFAULT": "0.375rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"},
            },
            },
        }
    </script>
</head>
<body class="bg-background-light dark:bg-background-dark text-text-primary dark:text-text-primary font-display">
<div class="relative flex min-h-screen w-full flex-col overflow-x-hidden">
<header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-dark-border dark:border-dark-border px-6 lg:px-40 py-4 bg-background-light dark:bg-background-dark/80 backdrop-blur-md sticky top-0 z-50">
<div class="flex items-center gap-3 text-text-primary dark:text-text-primary">
<div class="size-8 text-primary">
<span class="material-symbols-outlined !text-[32px]">cut</span>
</div>
<h2 class="text-lg font-bold leading-tight tracking-[-0.015em]">SilentCut AI</h2>
</div>
<div class="hidden md:flex items-center gap-8">
<div class="flex items-center gap-6">
<a class="text-text-primary dark:text-text-primary text-sm font-medium hover:text-primary transition-colors" href="#features">Features</a>
<a class="text-text-primary dark:text-text-primary text-sm font-medium hover:text-primary transition-colors" href="#privacy">Privacy</a>
<a class="text-text-primary dark:text-text-primary text-sm font-medium hover:text-primary transition-colors" href="#pricing">Pricing</a>
</div>
<div class="flex gap-3">
<button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 border border-dark-border dark:border-dark-border bg-transparent text-text-primary dark:text-text-primary text-sm font-bold hover:bg-dark-panel dark:hover:bg-dark-panel transition-colors">
<span class="truncate">Log In</span>
</button>
<button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-9 px-4 bg-primary text-background-light text-sm font-bold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20">
<span class="truncate">Sign Up</span>
</button>
</div>
</div>
<div class="md:hidden text-text-primary dark:text-text-primary">
<span class="material-symbols-outlined">menu</span>
</div>
</header>
<section class="flex flex-col items-center justify-center px-6 lg:px-40 pt-16 pb-20 overflow-hidden relative">
<div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary/20 blur-[120px] rounded-full pointer-events-none -z-10"></div>
<div class="flex flex-col items-center max-w-[960px] text-center gap-8">
<div class="flex flex-col gap-4">
<div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-wide w-fit mx-auto">
<span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                    v2.0 Now Available
                </div>
<h1 class="text-4xl md:text-6xl font-black leading-tight tracking-[-0.033em] text-text-primary dark:text-text-primary">
                    Cut the Noise, <span class="text-primary">Keep the Privacy.</span>
</h1>
<p class="text-text-secondary dark:text-text-secondary text-lg md:text-xl font-normal leading-relaxed max-w-[720px] mx-auto">
                    Automatically remove silences and filler words in seconds. 100% local processing ensures your footage never leaves your device.
                </p>
</div>
<div class="flex flex-wrap justify-center gap-4">
<button class="flex min-w-[160px] cursor-pointer items-center justify-center rounded-lg h-12 px-6 bg-primary text-background-light text-base font-bold hover:bg-primary/90 transition-all shadow-lg shadow-primary/25 hover:shadow-primary/40 transform hover:-translate-y-0.5">
                    Start Editing for Free
                </button>
<button class="flex min-w-[160px] cursor-pointer items-center justify-center rounded-lg h-12 px-6 border border-dark-border dark:border-dark-border bg-dark-panel dark:bg-dark-panel text-text-primary dark:text-text-primary text-base font-bold hover:bg-dark-border dark:hover:bg-dark-border transition-all">
<span class="material-symbols-outlined mr-2 !text-[20px]">play_circle</span>
                    Watch Demo
                </button>
</div>
<div class="flex items-center gap-6 mt-4 text-sm text-text-secondary dark:text-text-secondary">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined !text-[18px] text-primary">check_circle</span>
<span>No Cloud Upload</span>
</div>
<div class="flex items-center gap-2">
<span class="material-symbols-outlined !text-[18px] text-primary">check_circle</span>
<span>Works Offline</span>
</div>
<div class="flex items-center gap-2">
<span class="material-symbols-outlined !text-[18px] text-primary">check_circle</span>
<span>Mac &amp; Windows</span>
</div>
</div>
<div class="mt-12 w-full relative group">
<div class="absolute inset-0 bg-primary/20 blur-xl rounded-xl -z-10 group-hover:bg-primary/30 transition-all duration-500"></div>
<div class="w-full bg-dark-panel rounded-xl border border-dark-border shadow-2xl overflow-hidden aspect-video relative">
<div class="absolute inset-0 flex flex-col">
<div class="h-10 bg-dark-border border-b border-dark-border flex items-center px-4 gap-2">
<div class="flex gap-1.5">
<div class="w-3 h-3 rounded-full bg-[#ff4444]"></div>
<div class="w-3 h-3 rounded-full bg-[#fdd835]"></div>
<div class="w-3 h-3 rounded-full bg-primary"></div>
</div>
<div class="flex-1 text-center text-xs text-text-secondary font-mono">SilentCut Project - timeline_final.scut</div>
</div>
<div class="flex-1 flex bg-background-light relative">
<div class="w-16 border-r border-dark-border flex flex-col items-center py-4 gap-6 text-text-secondary">
<span class="material-symbols-outlined hover:text-text-primary cursor-pointer">folder_open</span>
<span class="material-symbols-outlined text-primary cursor-pointer">content_cut</span>
<span class="material-symbols-outlined hover:text-text-primary cursor-pointer">tune</span>
<span class="material-symbols-outlined hover:text-text-primary cursor-pointer">settings</span>
</div>
<div class="flex-1 flex flex-col p-4 gap-4">
<div class="flex-1 bg-black rounded-lg relative overflow-hidden flex items-center justify-center border border-dark-border">
<div class="absolute inset-0 opacity-40 bg-[url('https://images.unsplash.com/photo-1576858574144-9ae1ebcf5ae5?q=80&amp;w=2500&amp;auto=format&amp;fit=crop')] bg-cover bg-center" data-alt="Video editing software interface preview showing a person talking"></div>
<div class="z-10 bg-black/60 backdrop-blur-sm px-4 py-2 rounded-full text-text-primary text-sm flex items-center gap-2 border border-text-primary/10">
<span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span> Analyzing Audio...
                                     </div>
</div>
<div class="h-32 bg-dark-panel rounded-lg border border-dark-border relative overflow-hidden p-2 flex flex-col justify-center">
<div class="flex items-end gap-[2px] h-16 w-full opacity-80">
<div class="w-full h-full bg-[linear-gradient(90deg,transparent_0%,#00FF7F_10%,#00FF7F_25%,transparent_25%,transparent_35%,#00FF7F_35%,#00FF7F_60%,transparent_60%,transparent_70%,#00FF7F_70%,#00FF7F_100%)] opacity-50 absolute top-4 left-0 right-0 bottom-4"></div>
<div class="absolute inset-0 flex items-center">
<div class="w-[25%] h-full"></div>
<div class="w-[10%] h-full bg-secondary-accent/20 border-x border-secondary-accent/50 flex items-center justify-center">
<span class="text-[10px] text-secondary-accent font-mono">SILENCE</span>
</div>
<div class="w-[25%] h-full"></div>
<div class="w-[10%] h-full bg-secondary-accent/20 border-x border-secondary-accent/50 flex items-center justify-center">
<span class="text-[10px] text-secondary-accent font-mono">SILENCE</span>
</div>
</div>
</div>
<div class="w-full h-1 bg-dark-border mt-2 rounded-full relative">
<div class="absolute left-[30%] top-1/2 -translate-y-1/2 w-3 h-3 bg-primary rounded-full shadow cursor-pointer shadow-primary/50"></div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div></section>
<section class="py-20 px-6 lg:px-40 bg-dark-panel dark:bg-dark-panel border-y border-dark-border dark:border-dark-border" id="features">
<div class="max-w-[960px] mx-auto flex flex-col gap-16">
<div class="text-center max-w-[720px] mx-auto">
<h2 class="text-3xl md:text-4xl font-black leading-tight mb-4 text-text-primary dark:text-text-primary">Smart Editing, <span class="text-primary">Zero Data Leaks</span></h2>
<p class="text-text-secondary dark:text-text-secondary text-lg">Experience the speed of AI without compromising your footage security. We built SilentCut to be the fastest way to edit dialogue.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="flex flex-col gap-4 rounded-xl border border-dark-border dark:border-dark-border bg-background-light dark:bg-background-light p-6 hover:border-primary/50 transition-colors group">
<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-background-light transition-colors">
<span class="material-symbols-outlined !text-[28px]">graphic_eq</span>
</div>
<div class="flex flex-col gap-2">
<h3 class="text-xl font-bold text-text-primary dark:text-text-primary">Smart Silence Removal</h3>
<p class="text-text-secondary dark:text-text-secondary text-sm leading-relaxed">Automatically detect and cut silent pauses in seconds. Adjust threshold and padding to keep it natural.</p>
</div>
</div>
<div class="flex flex-col gap-4 rounded-xl border border-dark-border dark:border-dark-border bg-background-light dark:bg-background-light p-6 hover:border-primary/50 transition-colors group">
<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-background-light transition-colors">
<span class="material-symbols-outlined !text-[28px]">edit_note</span>
</div>
<div class="flex flex-col gap-2">
<h3 class="text-xl font-bold text-text-primary dark:text-text-primary">Text-Based Editing</h3>
<p class="text-text-secondary dark:text-text-secondary text-sm leading-relaxed">Edit your video by simply deleting words from the auto-generated transcript. It's as easy as editing a doc.</p>
</div>
</div>
<div class="flex flex-col gap-4 rounded-xl border border-dark-border dark:border-dark-border bg-background-light dark:bg-background-light p-6 hover:border-primary/50 transition-colors group">
<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-background-light transition-colors">
<span class="material-symbols-outlined !text-[28px]">security</span>
</div>
<div class="flex flex-col gap-2">
<h3 class="text-xl font-bold text-text-primary dark:text-text-primary">Local-First Privacy</h3>
<p class="text-text-secondary dark:text-text-secondary text-sm leading-relaxed">Your files never leave your device. All AI processing happens locally on your machine for ultimate security.</p>
</div>
</div>
</div>
</div>
</section>
<section class="py-20 px-6 lg:px-40 bg-background-light dark:bg-background-dark">
<div class="max-w-[960px] mx-auto">
<div class="flex flex-col md:flex-row gap-12 items-center">
<div class="flex-1 flex flex-col gap-6">
<h2 class="text-3xl font-black leading-tight text-text-primary dark:text-text-primary">From 2 hours of raw footage to a polished cut in minutes.</h2>
<p class="text-text-secondary dark:text-text-secondary">Stop scrubbing through hours of silence. Let our AI identify the good takes and remove the dead air instantly.</p>
<ul class="flex flex-col gap-4 mt-2">
<li class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary">check_circle</span>
<span class="text-text-primary dark:text-text-primary font-medium">Auto-ripple deletes</span>
</li>
<li class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary">check_circle</span>
<span class="text-text-primary dark:text-text-primary font-medium">Export XML to Premiere/DaVinci</span>
</li>
<li class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary">check_circle</span>
<span class="text-text-primary dark:text-text-primary font-medium">Customizable safety padding</span>
</li>
</ul>
</div>
<div class="flex-1 w-full bg-dark-panel p-6 rounded-2xl border border-dark-border shadow-2xl">
<div class="flex flex-col gap-6">
<div class="flex flex-col gap-2">
<div class="flex justify-between text-xs text-text-secondary uppercase font-bold tracking-wider">
<span>Raw Footage</span>
<span class="text-secondary-accent">10:00 min</span>
</div>
<div class="h-16 bg-background-light rounded border border-dark-border relative overflow-hidden flex items-center px-2 gap-1">
<div class="h-8 w-[10%] bg-text-secondary rounded-sm"></div>
<div class="h-[1px] w-[15%] bg-secondary-accent/30 border-t border-dotted border-secondary-accent"></div> 
<div class="h-10 w-[20%] bg-text-secondary rounded-sm"></div>
<div class="h-[1px] w-[10%] bg-secondary-accent/30 border-t border-dotted border-secondary-accent"></div> 
<div class="h-6 w-[15%] bg-text-secondary rounded-sm"></div>
<div class="h-[1px] w-[20%] bg-secondary-accent/30 border-t border-dotted border-secondary-accent"></div> 
<div class="h-8 w-[10%] bg-text-secondary rounded-sm"></div>
</div>
</div>
<div class="flex justify-center -my-3 z-10">
<div class="bg-primary rounded-full p-2 text-background-light shadow-lg">
<span class="material-symbols-outlined">arrow_downward</span>
</div>
</div>
<div class="flex flex-col gap-2">
<div class="flex justify-between text-xs text-text-secondary uppercase font-bold tracking-wider">
<span>AI Processed</span>
<span class="text-primary">4:20 min</span>
</div>
<div class="h-16 bg-background-light rounded border border-primary/30 shadow-[0_0_15px_rgba(0,255,127,0.15)] relative overflow-hidden flex items-center px-2 gap-[1px]">
<div class="h-8 w-[24%] bg-primary rounded-l-sm"></div>
<div class="h-10 w-[38%] bg-primary"></div>
<div class="h-6 w-[28%] bg-primary"></div>
<div class="h-8 w-[10%] bg-primary rounded-r-sm"></div>
</div>
</div>
</div>
</div>
</div>
</div>
</section>
<section class="py-20 px-6 lg:px-40 bg-dark-panel dark:bg-dark-panel border-t border-dark-border dark:border-dark-border" id="pricing">
<div class="max-w-[960px] mx-auto flex flex-col gap-12">
<div class="text-center">
<h2 class="text-3xl md:text-4xl font-black leading-tight mb-4 text-text-primary dark:text-text-primary">Simple, Transparent Pricing</h2>
<p class="text-text-secondary dark:text-text-secondary">Start for free, upgrade for power.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="flex flex-col gap-6 rounded-xl border border-dark-border dark:border-dark-border bg-background-light dark:bg-background-light p-8">
<div>
<h3 class="text-text-primary dark:text-text-primary text-lg font-bold">Free</h3>
<div class="flex items-baseline gap-1 mt-2 text-text-primary dark:text-text-primary">
<span class="text-4xl font-black tracking-tighter">$0</span>
<span class="text-sm font-medium opacity-60">/mo</span>
</div>
<p class="text-sm text-text-secondary dark:text-text-secondary mt-2">Perfect for hobbyists.</p>
</div>
<button class="w-full cursor-pointer rounded-lg h-10 px-4 border border-dark-border dark:border-dark-border bg-transparent text-text-primary dark:text-text-primary text-sm font-bold hover:bg-dark-panel dark:hover:bg-dark-panel transition-colors">
                        Download Now
                    </button>
<div class="flex flex-col gap-3">
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            Basic silence removal
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            720p Export
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-text-muted !text-[20px]">check</span>
                            Watermarked
                        </div>
</div>
</div>
<div class="flex flex-col gap-6 rounded-xl border-2 border-primary bg-background-light dark:bg-background-light p-8 relative shadow-2xl shadow-primary/10">
<div class="absolute top-0 right-0 bg-primary text-background-light text-xs font-bold px-3 py-1 rounded-bl-lg rounded-tr-lg">POPULAR</div>
<div>
<h3 class="text-text-primary dark:text-text-primary text-lg font-bold">Pro Creator</h3>
<div class="flex items-baseline gap-1 mt-2 text-text-primary dark:text-text-primary">
<span class="text-4xl font-black tracking-tighter">$18</span>
<span class="text-sm font-medium opacity-60">/mo</span>
</div>
<p class="text-sm text-text-secondary dark:text-text-secondary mt-2">For serious YouTubers.</p>
</div>
<button class="w-full cursor-pointer rounded-lg h-10 px-4 bg-primary text-background-light text-sm font-bold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/25">
                        Start Free Trial
                    </button>
<div class="flex flex-col gap-3">
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
<strong>Everything in Free</strong>
</div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            No Watermarks
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            4K Export
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            Advanced Word Filtering
                        </div>
</div>
</div>
<div class="flex flex-col gap-6 rounded-xl border border-dark-border dark:border-dark-border bg-background-light dark:bg-background-light p-8">
<div>
<h3 class="text-text-primary dark:text-text-primary text-lg font-bold">Studio</h3>
<div class="flex items-baseline gap-1 mt-2 text-text-primary dark:text-text-primary">
<span class="text-4xl font-black tracking-tighter">$45</span>
<span class="text-sm font-medium opacity-60">/mo</span>
</div>
<p class="text-sm text-text-secondary dark:text-text-secondary mt-2">Agencies &amp; Teams.</p>
</div>
<button class="w-full cursor-pointer rounded-lg h-10 px-4 border border-dark-border dark:border-dark-border bg-transparent text-text-primary dark:text-text-primary text-sm font-bold hover:bg-dark-panel dark:hover:bg-dark-panel transition-colors">
                        Contact Sales
                    </button>
<div class="flex flex-col gap-3">
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            Team Collaboration
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            API Access
                        </div>
<div class="text-sm flex gap-3 text-text-secondary dark:text-text-secondary">
<span class="material-symbols-outlined text-primary !text-[20px]">check</span>
                            Dedicated Support
                        </div>
</div>
</div>
</div>
</div>
</section>
<footer class="bg-background-light dark:bg-background-light border-t border-dark-border dark:border-dark-border pt-16 pb-8 px-6 lg:px-40">
<div class="max-w-[960px] mx-auto flex flex-col gap-12">
<div class="flex flex-col md:flex-row justify-between gap-8">
<div class="flex flex-col gap-4">
<div class="flex items-center gap-2 text-text-primary dark:text-text-primary">
<div class="size-6 text-primary">
<span class="material-symbols-outlined">cut</span>
</div>
<h2 class="text-lg font-bold">SilentCut AI</h2>
</div>
<p class="text-sm text-text-secondary max-w-xs">
                        The privacy-first video editor that saves you hours of work. Built for creators who value their time and data.
                    </p>
</div>
<div class="flex gap-12 flex-wrap">
<div class="flex flex-col gap-3">
<h4 class="text-sm font-bold text-text-primary dark:text-text-primary uppercase tracking-wider">Product</h4>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Features</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Pricing</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Download</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Changelog</a>
</div>
<div class="flex flex-col gap-3">
<h4 class="text-sm font-bold text-text-primary dark:text-text-primary uppercase tracking-wider">Resources</h4>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Documentation</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Community</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Blog</a>
</div>
<div class="flex flex-col gap-3">
<h4 class="text-sm font-bold text-text-primary dark:text-text-primary uppercase tracking-wider">Legal</h4>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Privacy Policy</a>
<a class="text-sm text-text-secondary hover:text-primary transition-colors" href="#">Terms of Service</a>
</div>
</div>
</div>
<div class="border-t border-dark-border dark:border-dark-border pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
<p class="text-sm text-text-secondary">© 2024 SilentCut AI Inc. All rights reserved.</p>
<div class="flex gap-4">
<a class="text-text-secondary hover:text-primary transition-colors" href="#"><span class="sr-only">Twitter</span>
<svg aria-hidden="true" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
<path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
</svg>
</a>
<a class="text-text-secondary hover:text-primary transition-colors" href="#"><span class="sr-only">GitHub</span>
<svg aria-hidden="true" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
<path clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" fill-rule="evenodd"></path>
</svg>
</a>
</div>
</div>
</div>
</footer>
</div>

</body></html>

<!-- Project Creation Flow -->
<!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Project Creation Flow - PrivacyCut AI</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;900&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        "primary": "#36e278",
                        "background-light": "#f6f8f7",
                        "background-dark": "#112117",
                        "surface-dark": "#1c2e24",
                        "surface-darker": "#16251d",
                    },
                    fontFamily: {
                        "display": ["Inter", "sans-serif"]
                    },
                    borderRadius: { "DEFAULT": "0.25rem", "lg": "0.5rem", "xl": "0.75rem", "2xl": "1rem", "full": "9999px" },
                },
            },
        }
    </script>
<style>
        /* Custom scrollbar for webkit */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #112117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #2a4034; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #36e278; 
        }
        
        .toggle-checkbox:checked {
            right: 0;
            border-color: #36e278;
        }
        .toggle-checkbox:checked + .toggle-label {
            background-color: #36e278;
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark font-display text-gray-900 dark:text-white antialiased min-h-screen flex flex-col overflow-x-hidden">
<!-- Top Navigation -->
<header class="w-full border-b border-[#29382f] bg-[#111714] sticky top-0 z-50">
<div class="px-6 md:px-10 py-3 flex items-center justify-between max-w-7xl mx-auto">
<div class="flex items-center gap-3">
<div class="text-primary">
<span class="material-symbols-outlined text-3xl">movie_filter</span>
</div>
<h1 class="text-white text-lg font-bold tracking-tight">PrivacyCut AI</h1>
</div>
<div class="flex items-center gap-6">
<div class="hidden md:flex items-center gap-2 text-[#9eb7a8] text-sm bg-surface-dark px-3 py-1.5 rounded-full border border-[#29382f]">
<span class="material-symbols-outlined text-base">lock</span>
<span>Local Processing Mode</span>
</div>
<div class="size-9 bg-surface-dark rounded-full overflow-hidden border border-[#29382f] cursor-pointer" data-alt="User profile avatar gradient" style="background: linear-gradient(135deg, #36e278 0%, #112117 100%);">
</div>
</div>
</div>
</header>
<!-- Main Content Area -->
<main class="flex-grow flex flex-col items-center justify-start py-8 px-4 md:px-8">
<div class="w-full max-w-4xl flex flex-col gap-8">
<!-- Progress Stepper -->
<div class="w-full">
<div class="flex items-center justify-between relative mb-8">
<div class="absolute left-0 top-1/2 transform -translate-y-1/2 w-full h-1 bg-surface-dark rounded-full -z-10"></div>
<!-- Step 1: Completed -->
<div class="flex flex-col items-center gap-2">
<div class="size-10 rounded-full bg-primary text-background-dark flex items-center justify-center font-bold border-4 border-background-dark shadow-lg">
<span class="material-symbols-outlined">check</span>
</div>
<span class="text-primary text-xs font-semibold uppercase tracking-wider">Upload</span>
</div>
<!-- Connector 1-2 (Active) -->
<div class="absolute left-[10%] top-1/2 transform -translate-y-1/2 w-[40%] h-1 bg-primary rounded-full -z-10"></div>
<!-- Step 2: Active -->
<div class="flex flex-col items-center gap-2">
<div class="size-10 rounded-full bg-primary text-background-dark flex items-center justify-center font-bold border-4 border-background-dark shadow-[0_0_15px_rgba(54,226,120,0.4)]">
                            2
                        </div>
<span class="text-white text-xs font-semibold uppercase tracking-wider">Details &amp; AI</span>
</div>
<!-- Step 3: Pending -->
<div class="flex flex-col items-center gap-2">
<div class="size-10 rounded-full bg-surface-dark text-gray-500 flex items-center justify-center font-bold border-4 border-background-dark">
                            3
                        </div>
<span class="text-gray-500 text-xs font-semibold uppercase tracking-wider">Review</span>
</div>
</div>
</div>
<!-- Header Text -->
<div class="text-center md:text-left">
<h2 class="text-3xl font-black text-white mb-2">Configure Project</h2>
<p class="text-[#9eb7a8]">Customize your video settings and select AI enhancements.</p>
</div>
<!-- Two Column Layout -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
<!-- Left Column: Source Video Context (Summary of Step 1) -->
<div class="lg:col-span-4 flex flex-col gap-4">
<div class="bg-surface-dark border border-[#29382f] rounded-xl p-4 flex flex-col gap-4">
<div class="flex items-center justify-between mb-2">
<h3 class="text-sm font-semibold text-white">Source Video</h3>
<button class="text-xs text-primary hover:underline">Change</button>
</div>
<div class="aspect-video w-full bg-black rounded-lg overflow-hidden relative group">
<div class="absolute inset-0 bg-cover bg-center opacity-60" data-alt="Abstract nature video thumbnail showing mountains" style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuB8sHmDkVvrLPRiAw1v_RgunKE5FfAWxbvGKQOSqC0CprRsamU2fN8veTwE54TuwuAhPXayJ7YJ6nfdWJHZIEMRa_YNnufDAFAuoFzQWkjQWOISrVUujvNgG3m8Irvk7r86jItmBjb9q0rof_MTH5dy3IIUN4-JoO0zrX87Ag6ri9EHJuhml5HnwIHlRXydDMy8FIJ4P_sP4REm6zc-T1OB6dOdnYacxkAuGMaqGz_48LnvRQN6YIovNFlcDEdE0PDacBAL7XKdHJFw");'>
</div>
<div class="absolute inset-0 flex items-center justify-center">
<span class="material-symbols-outlined text-white text-4xl opacity-80">play_circle</span>
</div>
</div>
<div class="flex items-start gap-3">
<div class="bg-surface-darker p-2 rounded text-[#9eb7a8]">
<span class="material-symbols-outlined text-xl">movie</span>
</div>
<div class="flex flex-col overflow-hidden">
<span class="text-white text-sm font-medium truncate">interview_recording_raw.mp4</span>
<span class="text-[#9eb7a8] text-xs">124 MB • 14:05 min</span>
</div>
</div>
</div>
<div class="bg-primary/5 border border-primary/20 rounded-xl p-4 flex items-start gap-3">
<span class="material-symbols-outlined text-primary text-xl mt-0.5">verified_user</span>
<div class="flex flex-col gap-1">
<p class="text-primary text-sm font-bold">Privacy Guaranteed</p>
<p class="text-[#9eb7a8] text-xs leading-relaxed">
                                Your video remains on your device. Our AI models run locally in your browser. No upload to cloud servers.
                            </p>
</div>
</div>
</div>
<!-- Right Column: Form Inputs & AI Settings -->
<div class="lg:col-span-8 flex flex-col gap-6">
<!-- Section: Basic Info -->
<div class="bg-surface-dark border border-[#29382f] rounded-xl p-6">
<div class="flex flex-col gap-5">
<!-- Project Name Input -->
<div class="flex flex-col gap-2">
<label class="text-white text-sm font-semibold" for="project-name">Project Name</label>
<input class="w-full bg-background-dark border border-[#29382f] rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all" id="project-name" placeholder="e.g. Weekly Vlog - Episode 4" type="text"/>
</div>
<!-- Aspect Ratio Selector -->
<div class="flex flex-col gap-2">
<label class="text-white text-sm font-semibold">Canvas Format</label>
<div class="grid grid-cols-3 gap-3">
<!-- 16:9 Option -->
<label class="cursor-pointer">
<input checked="" class="peer sr-only" name="aspect" type="radio"/>
<div class="flex flex-col items-center gap-2 p-3 rounded-lg border border-[#29382f] bg-background-dark peer-checked:border-primary peer-checked:bg-primary/10 transition-all hover:border-gray-500">
<div class="w-8 h-5 border-2 border-current rounded-sm text-gray-400 peer-checked:text-primary"></div>
<span class="text-xs font-medium text-gray-300 peer-checked:text-white">16:9 Landscape</span>
</div>
</label>
<!-- 9:16 Option -->
<label class="cursor-pointer">
<input class="peer sr-only" name="aspect" type="radio"/>
<div class="flex flex-col items-center gap-2 p-3 rounded-lg border border-[#29382f] bg-background-dark peer-checked:border-primary peer-checked:bg-primary/10 transition-all hover:border-gray-500">
<div class="w-5 h-8 border-2 border-current rounded-sm text-gray-400 peer-checked:text-primary"></div>
<span class="text-xs font-medium text-gray-300 peer-checked:text-white">9:16 Portrait</span>
</div>
</label>
<!-- 1:1 Option -->
<label class="cursor-pointer">
<input class="peer sr-only" name="aspect" type="radio"/>
<div class="flex flex-col items-center gap-2 p-3 rounded-lg border border-[#29382f] bg-background-dark peer-checked:border-primary peer-checked:bg-primary/10 transition-all hover:border-gray-500">
<div class="size-6 border-2 border-current rounded-sm text-gray-400 peer-checked:text-primary"></div>
<span class="text-xs font-medium text-gray-300 peer-checked:text-white">1:1 Square</span>
</div>
</label>
</div>
</div>
</div>
</div>
<!-- Section: AI Preferences -->
<div class="bg-surface-dark border border-[#29382f] rounded-xl p-6">
<div class="flex items-center gap-2 mb-6">
<span class="material-symbols-outlined text-primary">auto_fix_high</span>
<h3 class="text-white text-lg font-bold">AI Magic Tools</h3>
</div>
<div class="space-y-6">
<!-- Toggle 1: Silence Removal -->
<div class="flex items-center justify-between group">
<div class="flex items-start gap-4">
<div class="bg-background-dark p-2.5 rounded-lg text-primary">
<span class="material-symbols-outlined">graphic_eq</span>
</div>
<div>
<p class="text-white font-medium mb-1">Silence Removal</p>
<p class="text-[#9eb7a8] text-sm">Automatically cuts pauses longer than 0.5s.</p>
</div>
</div>
<label class="flex items-center cursor-pointer relative" for="silence-toggle">
<input checked="" class="sr-only peer" id="silence-toggle" type="checkbox"/>
<div class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
<hr class="border-[#29382f]"/>
<!-- Toggle 2: Profanity Filter -->
<div class="flex items-center justify-between group">
<div class="flex items-start gap-4">
<div class="bg-background-dark p-2.5 rounded-lg text-primary">
<span class="material-symbols-outlined">explicit</span>
</div>
<div>
<p class="text-white font-medium mb-1">Profanity Filter</p>
<p class="text-[#9eb7a8] text-sm">Mutes or beeps detected curse words.</p>
</div>
</div>
<label class="flex items-center cursor-pointer relative" for="profanity-toggle">
<input class="sr-only peer" id="profanity-toggle" type="checkbox"/>
<div class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
<hr class="border-[#29382f]"/>
<!-- Toggle 3: Auto Captions -->
<div class="flex items-center justify-between group">
<div class="flex items-start gap-4">
<div class="bg-background-dark p-2.5 rounded-lg text-primary">
<span class="material-symbols-outlined">closed_caption</span>
</div>
<div>
<p class="text-white font-medium mb-1">Auto Captions</p>
<p class="text-[#9eb7a8] text-sm">Generate subtitles from audio track.</p>
</div>
</div>
<label class="flex items-center cursor-pointer relative" for="captions-toggle">
<input class="sr-only peer" id="captions-toggle" type="checkbox"/>
<div class="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
</div>
</div>
</div>
</div>
<!-- Footer Navigation -->
<div class="flex items-center justify-between pt-6 border-t border-[#29382f] mt-2">
<button class="flex items-center gap-2 px-6 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-surface-dark transition-colors font-medium">
<span class="material-symbols-outlined text-lg">arrow_back</span>
                    Back
                </button>
<button class="flex items-center gap-2 px-8 py-3 rounded-lg bg-primary text-background-dark hover:bg-[#2dc466] transition-colors font-bold shadow-[0_0_20px_rgba(54,226,120,0.2)] hover:shadow-[0_0_25px_rgba(54,226,120,0.4)] transform hover:-translate-y-0.5 transition-all">
                    Next Step
                    <span class="material-symbols-outlined text-lg">arrow_forward</span>
</button>
</div>
</div>
</main>
</body></html>

<!-- Video Preview & Edit -->
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Video Preview &amp; Edit - Privacy-First Editor</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        emerald: {
                            950: '#022c22',
                            900: '#064e3b',
                            800: '#065f46',
                            700: '#047857',
                            600: '#059669',
                            500: '#10b981',
                            400: '#34d399',
                            300: '#6ee7b7',
                            200: '#a7f3d0',
                            100: '#d1fae5',
                            50: '#ecfdf5',
                        },
                        background: {
                            dark: "#050b08",
                            panel: "#0f1f18"
                        }
                    },
                    fontFamily: {
                        sans: ["Inter", "sans-serif"]
                    }
                }
            }
        };
    </script>
<style type="text/tailwindcss">
        :root {
            --primary-green: #10b981;
            --accent-green: #34d399;
            --dark-green-bg: #022c22;
        }
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }input[type=range] {
            -webkit-appearance: none;
            @apply bg-transparent;
        }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            @apply h-4 w-4 rounded-full bg-emerald-400 border-2 border-emerald-950 cursor-pointer -mt-1.5 shadow-lg shadow-emerald-500/50;
        }
        input[type=range]::-webkit-slider-runnable-track {
            @apply w-full h-1 cursor-pointer bg-emerald-900 rounded-full;
        }
    </style>
</head>
<body class="bg-background-dark font-sans text-slate-300 h-screen flex overflow-hidden selection:bg-emerald-500 selection:text-white">
<aside class="w-20 lg:w-64 bg-emerald-950 border-r border-emerald-900/50 flex flex-col justify-between shrink-0 z-20">
<div>
<div class="h-16 flex items-center px-6 border-b border-emerald-900/50 bg-emerald-950/50 backdrop-blur-sm">
<div class="flex items-center gap-3 text-emerald-400">
<span class="material-symbols-outlined text-3xl">verified_user</span>
<span class="font-bold text-lg tracking-tight text-white hidden lg:block">PrivEdit</span>
</div>
</div>
<nav class="p-4 space-y-2">
<a class="flex items-center gap-4 px-4 py-3 rounded-xl text-emerald-100/70 hover:bg-emerald-900/40 hover:text-emerald-300 transition-all group" href="#">
<span class="material-symbols-outlined group-hover:scale-110 transition-transform">dashboard</span>
<span class="font-medium hidden lg:block">Dashboard</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 rounded-xl bg-emerald-900/60 text-emerald-300 shadow-lg shadow-emerald-900/20 border border-emerald-800/50" href="#">
<span class="material-symbols-outlined">movie_edit</span>
<span class="font-medium hidden lg:block">Active Project</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 rounded-xl text-emerald-100/70 hover:bg-emerald-900/40 hover:text-emerald-300 transition-all group" href="#">
<span class="material-symbols-outlined group-hover:scale-110 transition-transform">folder_open</span>
<span class="font-medium hidden lg:block">Library</span>
</a>
<a class="flex items-center gap-4 px-4 py-3 rounded-xl text-emerald-100/70 hover:bg-emerald-900/40 hover:text-emerald-300 transition-all group" href="#">
<span class="material-symbols-outlined group-hover:scale-110 transition-transform">tune</span>
<span class="font-medium hidden lg:block">Settings</span>
</a>
</nav>
</div>
<div class="p-4 border-t border-emerald-900/50">
<button class="flex items-center gap-3 w-full px-2 py-2 rounded-xl hover:bg-emerald-900/40 transition-colors">
<div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-500 to-teal-400 ring-2 ring-emerald-950"></div>
<div class="text-left hidden lg:block">
<p class="text-sm font-medium text-emerald-100">Local User</p>
<p class="text-xs text-emerald-500">Pro Plan</p>
</div>
</button>
</div>
</aside>
<div class="flex-1 flex flex-col min-w-0 bg-background-dark relative">
<header class="h-16 bg-background-panel border-b border-emerald-900/30 flex items-center justify-between px-6 shrink-0 z-10">
<div class="flex items-center gap-4">
<h1 class="text-lg font-semibold text-emerald-50">Interview_Clip_01.mp4</h1>
<span class="px-2 py-0.5 rounded text-[10px] font-medium bg-emerald-900/50 text-emerald-400 border border-emerald-800/50 tracking-wider uppercase">Local Processing</span>
</div>
<div class="flex items-center gap-3">
<span class="text-xs text-emerald-600 mr-2 flex items-center gap-1">
<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    Auto-saved
                </span>
<button class="px-4 py-2 rounded-lg text-sm font-medium text-emerald-400 hover:text-emerald-300 hover:bg-emerald-900/30 transition-colors">
                    Discard
                </button>
<button class="px-5 py-2 rounded-lg text-sm font-medium bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/50 transition-all flex items-center gap-2">
<span>Export</span>
<span class="material-symbols-outlined text-sm">ios_share</span>
</button>
</div>
</header>
<main class="flex-1 overflow-hidden flex flex-col p-4 lg:p-6 gap-6">
<div class="flex-1 min-h-0 flex justify-center relative bg-black/40 rounded-2xl border border-emerald-900/30 overflow-hidden group">
<div class="relative h-full aspect-video bg-black shadow-2xl">
<img alt="Video Preview" class="w-full h-full object-cover opacity-90" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBmJF0e9n5ewS-L3WzWcemZZU8QN0p99Dn8F1ksPq62pWB9xHKD9CxliRuoKlNjbvWy5YgryoPcVcd-RtiwBqKEiK94aKzS4c7PgzrSUZem9PL3UISKnT1zydNyxYcmkXHW-yKb6p30BDWSCSF4LNRsNSRBWFo2e-0QXkyYS_CcdLy-j4NFYBp-hFuJVcksHBmuXhqhJBeqEjDQ8Ln8hRqeUIYp2yFuYt9nBe4eP42bcFVBlsKWmVJACEpv7iIqepOYAGjocMCzCtJK"/>
<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-between p-6">
<div class="flex justify-between items-start">
<div class="bg-black/60 backdrop-blur px-3 py-1 rounded text-xs font-mono text-emerald-400 border border-emerald-900/50">1080p • 60fps</div>
</div>
<div class="absolute inset-0 flex items-center justify-center pointer-events-none">
<button class="w-20 h-20 rounded-full bg-emerald-500/20 backdrop-blur-sm border border-emerald-400/30 flex items-center justify-center text-white pointer-events-auto hover:scale-110 hover:bg-emerald-500/40 transition-all shadow-[0_0_30px_rgba(16,185,129,0.3)]">
<span class="material-symbols-outlined text-5xl ml-1">play_arrow</span>
</button>
</div>
</div>
</div>
</div>
<div class="h-auto shrink-0 bg-background-panel border border-emerald-900/30 rounded-2xl p-5 shadow-2xl relative z-20">
<div class="flex justify-between items-center mb-4 px-1">
<div class="flex items-center gap-6">
<div class="text-sm font-medium text-emerald-100 flex items-center gap-2">
<span class="material-symbols-outlined text-emerald-500">graphic_eq</span>
                            Audio Timeline
                        </div>
<div class="h-4 w-px bg-emerald-800"></div>
<div class="flex gap-4 text-xs">
<div class="flex items-center gap-2 cursor-help" title="Low volume segments">
<div class="w-2 h-2 rounded-sm bg-emerald-900 ring-1 ring-emerald-700"></div>
<span class="text-emerald-400/80">Silence</span>
</div>
<div class="flex items-center gap-2 cursor-help" title="Detected filler words like 'um', 'ah'">
<div class="w-2 h-2 rounded-sm bg-emerald-500/50 ring-1 ring-emerald-400"></div>
<span class="text-emerald-400/80">Filtered Words</span>
</div>
</div>
</div>
<div class="flex items-center gap-2 text-emerald-400 font-mono text-sm bg-emerald-950/50 px-3 py-1 rounded border border-emerald-900/50">
<span>00:45</span>
<span class="text-emerald-700">/</span>
<span class="text-emerald-600">01:30</span>
</div>
</div>
<div class="relative h-24 bg-emerald-950/30 rounded-lg border border-emerald-900/40 overflow-hidden mb-6 group select-none">
<div class="absolute top-0 w-full h-full pointer-events-none z-0">
<div class="absolute left-[20%] h-full w-px border-r border-dashed border-emerald-900/40"></div>
<div class="absolute left-[40%] h-full w-px border-r border-dashed border-emerald-900/40"></div>
<div class="absolute left-[60%] h-full w-px border-r border-dashed border-emerald-900/40"></div>
<div class="absolute left-[80%] h-full w-px border-r border-dashed border-emerald-900/40"></div>
</div>
<div class="absolute left-1/2 top-0 bottom-0 w-0.5 bg-emerald-400 z-30 shadow-[0_0_10px_rgba(52,211,153,0.5)]">
<div class="absolute -top-1 -left-[5px] w-3 h-3 bg-emerald-400 rotate-45 rounded-sm"></div>
</div>
<div class="absolute inset-0 flex items-center px-4 gap-[2px]">
<div class="flex items-center gap-[2px] h-full flex-grow opacity-60 w-1/4">
<script>
                                for(let i=0; i<35; i++) {
                                    let h = Math.floor(Math.random() * 50) + 20;
                                    document.write(`<div class="w-1.5 bg-emerald-700 rounded-full hover:bg-emerald-500 transition-colors duration-75" style="height: ${h}%"></div>`);
                                }
                            </script>
</div>
<div class="relative flex items-center justify-center gap-[2px] h-full w-[15%] bg-emerald-900/20 mx-1 rounded group/segment border-x border-emerald-800/30">
<div class="absolute top-2 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider bg-emerald-900/80 text-emerald-500/70 border border-emerald-800 backdrop-blur-sm z-10 opacity-0 group-hover/segment:opacity-100 transition-opacity pointer-events-none">Silence</div>
<script>
                                for(let i=0; i<15; i++) {
                                    let h = Math.floor(Math.random() * 10) + 5; // Low height
                                    document.write(`<div class="w-1.5 bg-emerald-900 rounded-full opacity-50" style="height: ${h}%"></div>`);
                                }
                            </script>
</div>
<div class="relative flex items-center justify-center gap-[2px] h-full w-[10%] bg-emerald-500/10 mx-1 rounded group/segment border-x border-emerald-500/30 hover:bg-emerald-500/20 transition-colors cursor-pointer">
<div class="absolute bottom-2 px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 backdrop-blur-sm z-10">Removed</div>
<script>
                                for(let i=0; i<8; i++) {
                                    let h = Math.floor(Math.random() * 60) + 30;
                                    document.write(`<div class="w-1.5 bg-emerald-400/60 rounded-full" style="height: ${h}%"></div>`);
                                }
                            </script>
</div>
<div class="flex items-center gap-[2px] h-full flex-grow opacity-60 w-1/3">
<script>
                                for(let i=0; i<45; i++) {
                                    let h = Math.floor(Math.random() * 70) + 20;
                                    document.write(`<div class="w-1.5 bg-emerald-700 rounded-full hover:bg-emerald-500 transition-colors duration-75" style="height: ${h}%"></div>`);
                                }
                            </script>
</div>
</div>
</div>
<div class="flex flex-col md:flex-row justify-between items-center gap-4">
<div class="flex items-center gap-4 order-2 md:order-1">
<button class="p-3 rounded-xl hover:bg-emerald-900/30 text-emerald-600 hover:text-emerald-400 transition-all">
<span class="material-symbols-outlined text-2xl">skip_previous</span>
</button>
<button class="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-700 text-white flex items-center justify-center shadow-lg shadow-emerald-900/50 hover:scale-105 active:scale-95 transition-all">
<span class="material-symbols-outlined text-3xl fill-current">play_arrow</span>
</button>
<button class="p-3 rounded-xl hover:bg-emerald-900/30 text-emerald-600 hover:text-emerald-400 transition-all">
<span class="material-symbols-outlined text-2xl">skip_next</span>
</button>
<div class="h-8 w-px bg-emerald-900/50 mx-2"></div>
<div class="flex items-center bg-emerald-950/30 rounded-lg p-1 border border-emerald-900/30">
<button class="p-1.5 rounded hover:bg-emerald-900/50 text-emerald-500 transition-colors">
<span class="material-symbols-outlined text-lg">zoom_out</span>
</button>
<input class="w-20 h-1 bg-emerald-900 rounded-lg appearance-none cursor-pointer mx-2 accent-emerald-500" type="range"/>
<button class="p-1.5 rounded hover:bg-emerald-900/50 text-emerald-500 transition-colors">
<span class="material-symbols-outlined text-lg">zoom_in</span>
</button>
</div>
</div>
<div class="flex gap-3 order-1 md:order-2 w-full md:w-auto">
<button class="flex-1 md:flex-none flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-emerald-950 hover:bg-emerald-900 text-emerald-400 border border-emerald-900 hover:border-emerald-700 transition-all group">
<span class="material-symbols-outlined text-xl group-hover:text-emerald-300">content_cut</span>
<span class="text-sm font-medium">Cut Silence</span>
<span class="text-xs bg-emerald-900 text-emerald-500 px-1.5 py-0.5 rounded ml-1 border border-emerald-800">15</span>
</button>
<button class="flex-1 md:flex-none flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-emerald-950 hover:bg-emerald-900 text-emerald-400 border border-emerald-900 hover:border-emerald-700 transition-all group">
<span class="material-symbols-outlined text-xl group-hover:text-emerald-300">filter_alt_off</span>
<span class="text-sm font-medium">Filter Words</span>
<span class="text-xs bg-emerald-900 text-emerald-500 px-1.5 py-0.5 rounded ml-1 border border-emerald-800">8</span>
</button>
</div>
</div>
</div>
</main>
</div>

</body></html>