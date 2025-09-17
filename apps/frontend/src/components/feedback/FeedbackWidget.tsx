/**
 * Feedback Widget Component
 * 
 * Provides easy feedback collection with rating and comment functionality.
 * Integrates with UserJourneyTracker for contextual feedback.
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, MessageCircle, Star, Send, AlertCircle, CheckCircle, Lightbulb } from 'lucide-react';
import UserJourneyTracker from '@/lib/user-journey-tracker';

interface FeedbackWidgetProps {
  isOpen: boolean;
  onClose: () => void;
  context?: {
    page: string;
    feature?: string;
    workflowStep?: string;
  };
}

type FeedbackType = 'bug_report' | 'feature_request' | 'usability_issue' | 'performance_issue' | 'general_feedback';

interface FeedbackData {
  type: FeedbackType;
  title: string;
  description: string;
  rating?: number;
  stepsToReproduce?: string;
  expectedBehavior?: string;
  actualBehavior?: string;
}

const feedbackTypes = [
  {
    id: 'bug_report' as FeedbackType,
    label: 'Bug Report',
    icon: AlertCircle,
    color: 'text-red-500',
    description: 'Something is broken or not working correctly'
  },
  {
    id: 'feature_request' as FeedbackType,
    label: 'Feature Request',
    icon: Lightbulb,
    color: 'text-yellow-500',
    description: 'Suggest a new feature or improvement'
  },
  {
    id: 'usability_issue' as FeedbackType,
    label: 'Usability Issue',
    icon: MessageCircle,
    color: 'text-blue-500',
    description: 'Something is confusing or hard to use'
  },
  {
    id: 'performance_issue' as FeedbackType,
    label: 'Performance Issue',
    icon: AlertCircle,
    color: 'text-orange-500',
    description: 'Something is slow or unresponsive'
  },
  {
    id: 'general_feedback' as FeedbackType,
    label: 'General Feedback',
    icon: MessageCircle,
    color: 'text-gray-500',
    description: 'General comments or suggestions'
  }
];

const FeedbackWidget: React.FC<FeedbackWidgetProps> = ({ isOpen, onClose, context }) => {
  const [step, setStep] = useState<'type' | 'details' | 'submitting' | 'success'>('type');
  const [selectedType, setSelectedType] = useState<FeedbackType | null>(null);
  const [formData, setFormData] = useState<FeedbackData>({
    type: 'general_feedback',
    title: '',
    description: '',
    rating: undefined
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Reset form when widget opens
  useEffect(() => {
    if (isOpen) {
      setStep('type');
      setSelectedType(null);
      setFormData({
        type: 'general_feedback',
        title: '',
        description: '',
        rating: undefined
      });
      setErrors({});
    }
  }, [isOpen]);

  const handleTypeSelection = (type: FeedbackType) => {
    setSelectedType(type);
    setFormData(prev => ({ ...prev, type }));
    setStep('details');
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length < 5) {
      newErrors.title = 'Title must be at least 5 characters';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    } else if (formData.description.length < 10) {
      newErrors.description = 'Description must be at least 10 characters';
    }

    if (formData.type === 'bug_report') {
      if (!formData.stepsToReproduce?.trim()) {
        newErrors.stepsToReproduce = 'Steps to reproduce are required for bug reports';
      }
      if (!formData.expectedBehavior?.trim()) {
        newErrors.expectedBehavior = 'Expected behavior is required for bug reports';
      }
      if (!formData.actualBehavior?.trim()) {
        newErrors.actualBehavior = 'Actual behavior is required for bug reports';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setIsSubmitting(true);
    setStep('submitting');

    try {
      // Get user journey tracker instance
      const tracker = UserJourneyTracker.getInstance();
      const sessionSummary = tracker.getSessionSummary();

      // Collect browser information
      const browserInfo = {
        userAgent: navigator.userAgent,
        viewport: `${window.innerWidth}x${window.innerHeight}`,
        screen: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: navigator.language,
        cookiesEnabled: navigator.cookieEnabled,
        onlineStatus: navigator.onLine
      };

      // Prepare feedback payload
      const feedbackPayload = {
        session_id: sessionSummary.sessionId,
        user_id: sessionSummary.userId,
        feedback_type: formData.type,
        title: formData.title,
        description: formData.description,
        rating: formData.rating,
        page_url: window.location.href,
        user_agent: navigator.userAgent,
        browser_info: browserInfo,
        steps_to_reproduce: formData.stepsToReproduce,
        expected_behavior: formData.expectedBehavior,
        actual_behavior: formData.actualBehavior,
        tags: [
          ...(context?.feature ? [context.feature] : []),
          ...(context?.workflowStep ? [`workflow-${context.workflowStep}`] : []),
          `page-${context?.page || 'unknown'}`
        ]
      };

      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(feedbackPayload)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Track feedback submission
      tracker.trackAction({
        actionType: 'feedback_submitted',
        element: 'feedback-widget',
        metadata: {
          feedbackId: result.id,
          feedbackType: formData.type,
          rating: formData.rating,
          hasStepsToReproduce: !!formData.stepsToReproduce
        }
      });

      setStep('success');
      
      // Auto-close after success
      setTimeout(() => {
        onClose();
      }, 3000);

    } catch (error) {
      console.error('Failed to submit feedback:', error);
      setErrors({ submit: 'Failed to submit feedback. Please try again.' });
      setStep('details');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleRatingClick = (rating: number) => {
    setFormData(prev => ({ ...prev, rating }));
  };

  const renderStarRating = () => (
    <div className="flex items-center space-x-1">
      <span className="text-sm font-medium text-gray-700">Rate your experience:</span>
      <div className="flex space-x-1 ml-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => handleRatingClick(star)}
            className={`w-6 h-6 transition-colors ${
              formData.rating && star <= formData.rating
                ? 'text-yellow-400'
                : 'text-gray-300 hover:text-yellow-400'
            }`}
          >
            <Star fill="currentColor" />
          </button>
        ))}
      </div>
    </div>
  );

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
        onClick={(e) => e.target === e.currentTarget && onClose()}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-hidden"
        >
          {/* Header */}
          <div className="bg-gray-50 px-6 py-4 border-b flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <MessageCircle className="w-5 h-5 text-blue-500" />
              <h3 className="text-lg font-semibold text-gray-900">
                {step === 'type' && 'What kind of feedback do you have?'}
                {step === 'details' && 'Tell us more'}
                {step === 'submitting' && 'Submitting feedback...'}
                {step === 'success' && 'Thank you!'}
              </h3>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              disabled={isSubmitting}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
            {/* Step 1: Type Selection */}
            {step === 'type' && (
              <div className="space-y-3">
                {feedbackTypes.map((type) => {
                  const IconComponent = type.icon;
                  return (
                    <button
                      key={type.id}
                      onClick={() => handleTypeSelection(type.id)}
                      className="w-full text-left p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors group"
                    >
                      <div className="flex items-start space-x-3">
                        <IconComponent className={`w-5 h-5 mt-1 ${type.color} group-hover:scale-110 transition-transform`} />
                        <div>
                          <h4 className="font-medium text-gray-900 group-hover:text-blue-900">
                            {type.label}
                          </h4>
                          <p className="text-sm text-gray-600 mt-1">
                            {type.description}
                          </p>
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Step 2: Details Form */}
            {step === 'details' && (
              <div className="space-y-4">
                {context && (
                  <div className="bg-blue-50 p-3 rounded-lg text-sm">
                    <p className="text-blue-800">
                      <strong>Context:</strong> {context.page}
                      {context.feature && ` → ${context.feature}`}
                      {context.workflowStep && ` (Step: ${context.workflowStep})`}
                    </p>
                  </div>
                )}

                {/* Rating */}
                <div className="space-y-2">
                  {renderStarRating()}
                </div>

                {/* Title */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Title *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.title ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder="Brief summary of your feedback"
                    maxLength={200}
                  />
                  {errors.title && (
                    <p className="text-sm text-red-600">{errors.title}</p>
                  )}
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-700">
                    Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                    className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.description ? 'border-red-300' : 'border-gray-300'
                    }`}
                    placeholder="Please provide details about your feedback"
                    rows={4}
                    maxLength={5000}
                  />
                  {errors.description && (
                    <p className="text-sm text-red-600">{errors.description}</p>
                  )}
                  <p className="text-xs text-gray-500">
                    {formData.description.length}/5000 characters
                  </p>
                </div>

                {/* Bug Report Specific Fields */}
                {formData.type === 'bug_report' && (
                  <>
                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Steps to Reproduce *
                      </label>
                      <textarea
                        value={formData.stepsToReproduce || ''}
                        onChange={(e) => setFormData(prev => ({ ...prev, stepsToReproduce: e.target.value }))}
                        className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                          errors.stepsToReproduce ? 'border-red-300' : 'border-gray-300'
                        }`}
                        placeholder="1. First step&#10;2. Second step&#10;3. ..."
                        rows={3}
                      />
                      {errors.stepsToReproduce && (
                        <p className="text-sm text-red-600">{errors.stepsToReproduce}</p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Expected Behavior *
                      </label>
                      <textarea
                        value={formData.expectedBehavior || ''}
                        onChange={(e) => setFormData(prev => ({ ...prev, expectedBehavior: e.target.value }))}
                        className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                          errors.expectedBehavior ? 'border-red-300' : 'border-gray-300'
                        }`}
                        placeholder="What should have happened?"
                        rows={2}
                      />
                      {errors.expectedBehavior && (
                        <p className="text-sm text-red-600">{errors.expectedBehavior}</p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <label className="block text-sm font-medium text-gray-700">
                        Actual Behavior *
                      </label>
                      <textarea
                        value={formData.actualBehavior || ''}
                        onChange={(e) => setFormData(prev => ({ ...prev, actualBehavior: e.target.value }))}
                        className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                          errors.actualBehavior ? 'border-red-300' : 'border-gray-300'
                        }`}
                        placeholder="What actually happened?"
                        rows={2}
                      />
                      {errors.actualBehavior && (
                        <p className="text-sm text-red-600">{errors.actualBehavior}</p>
                      )}
                    </div>
                  </>
                )}

                {errors.submit && (
                  <div className="bg-red-50 border border-red-200 rounded-md p-3">
                    <p className="text-sm text-red-600">{errors.submit}</p>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={() => setStep('type')}
                    className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                    disabled={isSubmitting}
                  >
                    Back
                  </button>
                  <button
                    onClick={handleSubmit}
                    disabled={isSubmitting}
                    className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    <Send className="w-4 h-4" />
                    <span>Submit Feedback</span>
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Submitting */}
            {step === 'submitting' && (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Submitting your feedback...</p>
              </div>
            )}

            {/* Step 4: Success */}
            {step === 'success' && (
              <div className="text-center py-8">
                <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <h4 className="text-lg font-semibold text-gray-900 mb-2">
                  Thank you for your feedback!
                </h4>
                <p className="text-gray-600 mb-4">
                  We appreciate your input and will review it carefully.
                </p>
                <p className="text-sm text-gray-500">
                  This window will close automatically in a few seconds.
                </p>
              </div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default FeedbackWidget;
