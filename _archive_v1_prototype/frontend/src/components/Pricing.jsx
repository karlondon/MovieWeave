import React from 'react';
import { Check, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Pricing() {
  const plans = [
    {
      name: 'Starter',
      price: 'FREE',
      description: 'Perfect for testing',
      features: [
        '5 free videos/month',
        'Up to 100MB PDF files',
        'Standard animations',
        'Email support',
        'Basic tracking'
      ],
      cta: 'Start Free',
      highlighted: false
    },
    {
      name: 'Professional',
      price: '£5',
      period: 'per video',
      description: 'For serious creators',
      features: [
        'Unlimited videos',
        'Up to 500MB PDF files',
        'Premium animations',
        'Priority support',
        'Advanced analytics',
        'Batch processing',
        'Custom branding'
      ],
      cta: 'Get Started',
      highlighted: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      description: 'For studios',
      features: [
        'Everything in Pro',
        'Dedicated account manager',
        'Custom integrations',
        'API access',
        'White-label options',
        'SLA guarantee',
        '24/7 support'
      ],
      cta: 'Contact Sales',
      highlighted: false
    }
  ];

  return (
    <div className="min-h-[calc(100vh-64px)] py-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            Start free and scale as you grow. No hidden fees.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`card-hover rounded-xl p-8 transition-all duration-300 ${
                plan.highlighted
                  ? 'bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-2 border-indigo-500/50 transform md:scale-105'
                  : 'bg-slate-800/50 border border-slate-700/50'
              }`}
            >
              {plan.highlighted && (
                <div className="flex items-center gap-2 mb-4 text-indigo-400">
                  <Zap className="w-5 h-5" />
                  <span className="text-sm font-semibold">MOST POPULAR</span>
                </div>
              )}

              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <div className="mb-2">
                <span className="text-4xl font-bold">{plan.price}</span>
                {plan.period && <span className="text-slate-400 ml-2">{plan.period}</span>}
              </div>
              <p className="text-slate-400 text-sm mb-6">{plan.description}</p>

              <Link
                to="/dashboard"
                className={`block w-full py-3 px-4 rounded-lg font-semibold text-center mb-8 transition ${
                  plan.highlighted
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white hover:shadow-lg'
                    : 'bg-slate-700 text-white hover:bg-slate-600'
                }`}
              >
                {plan.cta}
              </Link>

              <div className="space-y-4">
                {plan.features.map((feature, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    <span className="text-slate-300">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* FAQ */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
          
          <div className="space-y-6">
            {[
              {
                q: 'Can I upgrade or downgrade anytime?',
                a: 'Yes! You can change your plan or pay-per-video at any time with no penalties.'
              },
              {
                q: 'What file formats do you support?',
                a: 'Currently we support PDF files up to 500MB. More formats coming soon!'
              },
              {
                q: 'How long does video generation take?',
                a: 'Most videos are ready in 2-5 minutes, depending on the length and complexity.'
              },
              {
                q: 'Is my content secure?',
                a: 'Yes! All files are encrypted and stored securely on AWS S3. We never share your content.'
              }
            ].map((item, i) => (
              <div key={i} className="bg-slate-800/50 border border-slate-700/50 rounded-lg p-6">
                <h4 className="font-semibold text-lg mb-2">{item.q}</h4>
                <p className="text-slate-400">{item.a}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
