"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Eye, EyeOff, Mail, Lock, User, ArrowRight, Scissors } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/stores/auth-store";

const registerSchema = z
  .object({
    full_name: z.string().min(2, "Name must be at least 2 characters"),
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    confirmPassword: z.string(),
    terms: z.boolean().refine((val) => val === true, {
      message: "You must accept the terms and conditions",
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  });

type RegisterFormData = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const { register: registerUser, isLoading } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    setError(null);
    try {
      await registerUser({
        email: data.email,
        password: data.password,
        full_name: data.full_name,
      });
      router.push("/dashboard");
    } catch {
      setError("Registration failed. Please try again.");
    }
  };

  return (
    <div className="relative z-10 flex-1 flex flex-col justify-center items-center p-4 sm:p-6 lg:p-8">
      {/* Decorative Background Elements */}
      <div className="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] bg-primary/10 rounded-full blur-[100px] opacity-60" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[30rem] h-[30rem] bg-purple-500/10 rounded-full blur-[100px] opacity-40" />
      </div>

      {/* Main Card Container */}
      <div className="w-full max-w-[500px] flex flex-col gap-6 relative z-10">
        {/* Logo Header */}
        <div className="flex items-center justify-center gap-3 mb-2">
          <div className="flex items-center gap-3 text-foreground">
            <div className="size-8 text-primary">
              <Scissors className="h-8 w-8" />
            </div>
            <h2 className="text-lg font-bold leading-tight tracking-[-0.015em]">ClipFlow</h2>
          </div>
        </div>

        {/* Card */}
        <div className="bg-card border border-border shadow-2xl rounded-2xl p-6 sm:p-10 backdrop-blur-sm">
          {/* Heading Group */}
          <div className="flex flex-col gap-2 mb-8 text-center">
            <h1 className="text-foreground text-3xl font-black leading-tight tracking-[-0.033em]">
              Create Your Account
            </h1>
            <p className="text-muted-foreground text-base font-normal leading-normal">
              Join thousands using AI-powered editing with end-to-end encryption.
            </p>
          </div>

          {/* Registration Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
            {error && (
              <div className="p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive text-sm">
                {error}
              </div>
            )}

            {/* Full Name */}
            <div className="flex flex-col gap-2">
              <Label htmlFor="full_name">Full Name</Label>
              <Input
                id="full_name"
                type="text"
                placeholder="Enter your full name"
                icon={<User className="h-5 w-5" />}
                error={errors.full_name?.message}
                {...register("full_name")}
              />
            </div>

            {/* Work Email */}
            <div className="flex flex-col gap-2">
              <Label htmlFor="email">Work Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="name@company.com"
                icon={<Mail className="h-5 w-5" />}
                error={errors.email?.message}
                {...register("email")}
              />
            </div>

            {/* Password Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="flex flex-col gap-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Min. 8 characters"
                    icon={<Lock className="h-5 w-5" />}
                    className="pr-12"
                    error={errors.password?.message}
                    {...register("password")}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-0 top-0 h-12 w-12 flex items-center justify-center text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    placeholder="Re-enter password"
                    icon={<Lock className="h-5 w-5" />}
                    className="pr-12"
                    error={errors.confirmPassword?.message}
                    {...register("confirmPassword")}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-0 top-0 h-12 w-12 flex items-center justify-center text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Terms Checkbox */}
            <div className="flex items-start gap-3 mt-1">
              <div className="flex h-5 items-center">
                <input
                  type="checkbox"
                  id="terms"
                  className="h-4 w-4 rounded border-border bg-card text-primary focus:ring-primary focus:ring-offset-card focus:ring-offset-1"
                  {...register("terms")}
                />
              </div>
              <div className="text-sm leading-5">
                <label htmlFor="terms" className="font-normal text-muted-foreground">
                  I agree to the{" "}
                  <Link
                    href="#"
                    className="font-medium text-foreground hover:underline decoration-primary decoration-2 underline-offset-4"
                  >
                    Terms and Conditions
                  </Link>{" "}
                  and{" "}
                  <Link
                    href="#"
                    className="font-medium text-foreground hover:underline decoration-primary decoration-2 underline-offset-4"
                  >
                    Privacy Policy
                  </Link>
                  .
                </label>
                {errors.terms && (
                  <p className="text-destructive text-xs mt-1">{errors.terms.message}</p>
                )}
              </div>
            </div>

            {/* Register Button */}
            <Button type="submit" size="lg" className="mt-2 group" isLoading={isLoading}>
              <span>Create Account</span>
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Button>

            {/* Divider */}
            {/* <div className="relative flex py-2 items-center">
              <div className="flex-grow border-t border-border" />
              <span className="flex-shrink-0 mx-4 text-muted-foreground text-xs uppercase tracking-wider">
                Or register with
              </span>
              <div className="flex-grow border-t border-border" />
            </div> */}

            {/* Social Login */}
            {/* <div className="grid grid-cols-2 gap-4">
              <Button type="button" variant="outline" className="h-10">
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                  <path
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    fill="#4285F4"
                  />
                  <path
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    fill="#34A853"
                  />
                  <path
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.26.81-.58z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                    fill="#EA4335"
                  />
                </svg>
                Google
              </Button>
              <Button type="button" variant="outline" className="h-10">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    clipRule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                    fillRule="evenodd"
                  />
                </svg>
                GitHub
              </Button>
            </div> */}
          </form>

          {/* Footer Link */}
          <div className="mt-8 text-center">
            <p className="text-muted-foreground text-sm font-normal">
              Already have an account?
              <Link
                href="/login"
                className="text-primary hover:text-foreground transition-colors font-semibold ml-1"
              >
                Log In
              </Link>
            </p>
          </div>

          {/* Trust Badge */}
          {/* <div className="mt-8 flex justify-center">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-medium">
              <Lock className="h-3 w-3" />
              End-to-end encrypted
            </div>
          </div> */}
        </div>

        {/* Bottom Links */}
        <div className="flex justify-center gap-6 text-xs text-muted-foreground/60">
          <Link href="#" className="hover:text-muted-foreground transition-colors">
            Help Center
          </Link>
          <Link href="#" className="hover:text-muted-foreground transition-colors">
            Privacy
          </Link>
          <Link href="#" className="hover:text-muted-foreground transition-colors">
            Terms
          </Link>
        </div>
      </div>
    </div>
  );
}
