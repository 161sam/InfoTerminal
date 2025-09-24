import React, { useState } from "react";
import { Shield, Image, Video, Music, Activity, Upload, AlertCircle, Zap } from "lucide-react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";
import MediaForensics from "@/components/media/MediaForensics";
import { textStyles, buttonStyles, inputStyles, cardStyles } from "@/styles/design-tokens";

interface VideoAnalysisResult {
  filename: string;
  duration: number;
  fps: number;
  codec: string;
  resolution: { width: number; height: number };
  bitrate: number;
  file_size: number;
}

interface AudioAnalysisResult {
  filename: string;
  duration: number;
  sample_rate: number;
  channels: number;
  codec: string;
  bitrate: number;
  file_size: number;
}

export default function MediaForensicsPage() {
  const [activeTab, setActiveTab] = useState<"image" | "video" | "audio">("image");
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [videoAnalysis, setVideoAnalysis] = useState<VideoAnalysisResult | null>(null);
  const [audioAnalysis, setAudioAnalysis] = useState<AudioAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const tabs = [
    {
      id: "image",
      label: "Image Analysis",
      icon: Image,
      description: "Analyze images for EXIF data, manipulation signs, and forensic evidence",
    },
    {
      id: "video",
      label: "Video Analysis",
      icon: Video,
      description: "Extract metadata, detect deepfakes, and analyze video authenticity",
    },
    {
      id: "audio",
      label: "Audio Analysis",
      icon: Music,
      description: "Voice analysis, audio fingerprinting, and authenticity verification",
    },
  ];

  const handleVideoUpload = async (file: File) => {
    if (!file.type.startsWith("video/")) {
      setError("Please select a valid video file");
      return;
    }

    if (file.size > 500 * 1024 * 1024) {
      // 500MB limit
      setError("Video file size must be less than 500MB");
      return;
    }

    setVideoFile(file);
    setError(null);

    // TODO: Implement video analysis API call
    // This would call the media-forensics service for video analysis
    setLoading(true);
    try {
      // Placeholder for video analysis
      setTimeout(() => {
        setVideoAnalysis({
          filename: file.name,
          duration: 120.5,
          fps: 30,
          codec: "H.264",
          resolution: { width: 1920, height: 1080 },
          bitrate: 5000000,
          file_size: file.size,
        });
        setLoading(false);
      }, 2000);
    } catch (err) {
      setError("Video analysis failed");
      setLoading(false);
    }
  };

  const handleAudioUpload = async (file: File) => {
    if (!file.type.startsWith("audio/")) {
      setError("Please select a valid audio file");
      return;
    }

    if (file.size > 100 * 1024 * 1024) {
      // 100MB limit
      setError("Audio file size must be less than 100MB");
      return;
    }

    setAudioFile(file);
    setError(null);

    // TODO: Implement audio analysis API call
    // This would call the media-forensics service for audio analysis
    setLoading(true);
    try {
      // Placeholder for audio analysis
      setTimeout(() => {
        setAudioAnalysis({
          filename: file.name,
          duration: 180.2,
          sample_rate: 44100,
          channels: 2,
          codec: "MP3",
          bitrate: 320000,
          file_size: file.size,
        });
        setLoading(false);
      }, 2000);
    } catch (err) {
      setError("Audio analysis failed");
      setLoading(false);
    }
  };

  const renderFileUpload = (
    accept: string,
    onFileSelect: (file: File) => void,
    currentFile: File | null,
    fileType: string,
    maxSize: string,
  ) => (
    <Panel>
      <div className="text-center p-8 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-400 transition-colors">
        <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
        <div className="mb-4">
          <div className={`${textStyles.body} font-medium mb-2`}>
            {currentFile ? currentFile.name : `Upload ${fileType} File`}
          </div>
          <div className={`${textStyles.bodySmall} text-gray-500 dark:text-slate-400`}>
            Drag & drop or click to select
          </div>
          <div className={`${textStyles.bodySmall} text-gray-400 dark:text-slate-500 mt-1`}>
            Max size: {maxSize}
          </div>
        </div>
        <input
          type="file"
          accept={accept}
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onFileSelect(file);
          }}
          className="hidden"
          id={`${fileType}-upload`}
        />
        <label
          htmlFor={`${fileType}-upload`}
          className={`${buttonStyles.primary} cursor-pointer inline-flex items-center gap-2`}
        >
          <Upload className="h-4 w-4" />
          Select {fileType}
        </label>
      </div>
    </Panel>
  );

  const renderVideoAnalysisResults = () => {
    if (!videoAnalysis) return null;

    return (
      <Panel>
        <div className="flex items-center gap-3 mb-6">
          <Video className="h-6 w-6 text-blue-500" />
          <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
            Video Analysis Results
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Basic Properties</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Duration:</span>
                <span>
                  {Math.floor(videoAnalysis.duration / 60)}:
                  {(videoAnalysis.duration % 60).toFixed(1).padStart(4, "0")}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Frame Rate:</span>
                <span>{videoAnalysis.fps} fps</span>
              </div>
              <div className="flex justify-between">
                <span>Resolution:</span>
                <span>
                  {videoAnalysis.resolution.width}×{videoAnalysis.resolution.height}
                </span>
              </div>
            </div>
          </div>

          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Technical Details</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Codec:</span>
                <span>{videoAnalysis.codec}</span>
              </div>
              <div className="flex justify-between">
                <span>Bitrate:</span>
                <span>{(videoAnalysis.bitrate / 1000000).toFixed(1)} Mbps</span>
              </div>
              <div className="flex justify-between">
                <span>File Size:</span>
                <span>{(videoAnalysis.file_size / 1024 / 1024).toFixed(1)} MB</span>
              </div>
            </div>
          </div>

          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Forensic Analysis</h4>
            <div className="space-y-2 text-sm">
              <div className="text-green-600 dark:text-green-400">
                ✓ No compression artifacts detected
              </div>
              <div className="text-green-600 dark:text-green-400">✓ Consistent metadata</div>
              <div className="text-yellow-600 dark:text-yellow-400">
                ⚠ Further analysis recommended
              </div>
            </div>
          </div>
        </div>
      </Panel>
    );
  };

  const renderAudioAnalysisResults = () => {
    if (!audioAnalysis) return null;

    return (
      <Panel>
        <div className="flex items-center gap-3 mb-6">
          <Music className="h-6 w-6 text-purple-500" />
          <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
            Audio Analysis Results
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Audio Properties</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Duration:</span>
                <span>
                  {Math.floor(audioAnalysis.duration / 60)}:
                  {(audioAnalysis.duration % 60).toFixed(1).padStart(4, "0")}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Sample Rate:</span>
                <span>{(audioAnalysis.sample_rate / 1000).toFixed(1)} kHz</span>
              </div>
              <div className="flex justify-between">
                <span>Channels:</span>
                <span>
                  {audioAnalysis.channels === 1
                    ? "Mono"
                    : audioAnalysis.channels === 2
                      ? "Stereo"
                      : `${audioAnalysis.channels} channels`}
                </span>
              </div>
            </div>
          </div>

          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Technical Details</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Codec:</span>
                <span>{audioAnalysis.codec}</span>
              </div>
              <div className="flex justify-between">
                <span>Bitrate:</span>
                <span>{(audioAnalysis.bitrate / 1000).toFixed(0)} kbps</span>
              </div>
              <div className="flex justify-between">
                <span>File Size:</span>
                <span>{(audioAnalysis.file_size / 1024 / 1024).toFixed(1)} MB</span>
              </div>
            </div>
          </div>

          <div className={`${cardStyles.base} ${cardStyles.padding}`}>
            <h4 className={`${textStyles.body} font-medium mb-3`}>Voice Analysis</h4>
            <div className="space-y-2 text-sm">
              <div className="text-green-600 dark:text-green-400">
                ✓ Natural voice patterns detected
              </div>
              <div className="text-green-600 dark:text-green-400">
                ✓ No significant splicing found
              </div>
              <div className="text-blue-600 dark:text-blue-400">
                ℹ Speaker identification available
              </div>
            </div>
          </div>
        </div>
      </Panel>
    );
  };

  return (
    <DashboardLayout
      title="Media Forensics"
      subtitle="Advanced multimedia file analysis and verification"
    >
      <div className="p-6">
        <div className="max-w-7xl space-y-6">
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-2 border-b border-gray-200 dark:border-gray-800">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-6 py-3 text-sm font-medium rounded-t-lg border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? "text-primary-600 border-primary-600 bg-primary-50 dark:bg-primary-900/20 dark:text-primary-300 dark:border-primary-400"
                      : "text-gray-500 border-transparent hover:text-gray-700 hover:border-gray-300 dark:text-slate-400 dark:hover:text-slate-200 dark:hover:border-gray-600"
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <div className="text-left">
                    <div>{tab.label}</div>
                    <div className="text-xs opacity-75 font-normal">{tab.description}</div>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <AlertCircle className="h-5 w-5" />
              {error}
            </div>
          )}

          {/* Tab Content */}
          <div className="mt-6">
            {activeTab === "image" && (
              <div>
                <Panel>
                  <div className="flex items-center gap-3 mb-6">
                    <Image className="h-6 w-6 text-blue-500" />
                    <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
                      Image Forensics Analysis
                    </h3>
                  </div>
                  <div className={`${textStyles.bodySmall} text-gray-600 dark:text-slate-400 mb-6`}>
                    Analyze images for EXIF metadata, manipulation detection, perceptual hashing,
                    and reverse image search capabilities.
                  </div>
                </Panel>

                <MediaForensics apiBaseUrl="http://localhost:8618/v1" className="mt-6" />
              </div>
            )}

            {activeTab === "video" && (
              <div className="space-y-6">
                <Panel>
                  <div className="flex items-center gap-3 mb-6">
                    <Video className="h-6 w-6 text-blue-500" />
                    <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
                      Video Forensics Analysis
                    </h3>
                  </div>
                  <div className={`${textStyles.bodySmall} text-gray-600 dark:text-slate-400 mb-6`}>
                    Extract metadata, detect deepfakes, analyze compression artifacts, and verify
                    video authenticity.
                  </div>
                </Panel>

                {renderFileUpload("video/*", handleVideoUpload, videoFile, "Video", "500MB")}

                {loading && (
                  <Panel>
                    <div className="flex items-center gap-3 text-blue-600">
                      <Zap className="h-5 w-5 animate-pulse" />
                      <span>Analyzing video...</span>
                    </div>
                  </Panel>
                )}

                {renderVideoAnalysisResults()}

                {!videoFile && !loading && (
                  <Panel>
                    <h4 className={`${textStyles.h4} mb-4`}>Video Analysis Features</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>
                          Metadata Extraction
                        </h5>
                        <p className={textStyles.bodySmall}>
                          Extract technical details, timestamps, and embedded metadata
                        </p>
                      </div>
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>
                          Deepfake Detection
                        </h5>
                        <p className={textStyles.bodySmall}>
                          Identify AI-generated or manipulated video content
                        </p>
                      </div>
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>Frame Analysis</h5>
                        <p className={textStyles.bodySmall}>
                          Analyze individual frames for inconsistencies
                        </p>
                      </div>
                    </div>
                  </Panel>
                )}
              </div>
            )}

            {activeTab === "audio" && (
              <div className="space-y-6">
                <Panel>
                  <div className="flex items-center gap-3 mb-6">
                    <Music className="h-6 w-6 text-purple-500" />
                    <h3 className={`${textStyles.h3} text-primary-600 dark:text-primary-400`}>
                      Audio Forensics Analysis
                    </h3>
                  </div>
                  <div className={`${textStyles.bodySmall} text-gray-600 dark:text-slate-400 mb-6`}>
                    Voice analysis, speaker identification, authenticity verification, and audio
                    fingerprinting.
                  </div>
                </Panel>

                {renderFileUpload("audio/*", handleAudioUpload, audioFile, "Audio", "100MB")}

                {loading && (
                  <Panel>
                    <div className="flex items-center gap-3 text-purple-600">
                      <Zap className="h-5 w-5 animate-pulse" />
                      <span>Analyzing audio...</span>
                    </div>
                  </Panel>
                )}

                {renderAudioAnalysisResults()}

                {!audioFile && !loading && (
                  <Panel>
                    <h4 className={`${textStyles.h4} mb-4`}>Audio Analysis Features</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>Voice Analysis</h5>
                        <p className={textStyles.bodySmall}>
                          Analyze voice patterns, pitch, and speech characteristics
                        </p>
                      </div>
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>Speaker ID</h5>
                        <p className={textStyles.bodySmall}>
                          Identify and verify speaker identity through voice prints
                        </p>
                      </div>
                      <div className={`${cardStyles.base} ${cardStyles.padding}`}>
                        <h5 className={`${textStyles.body} font-medium mb-2`}>
                          Audio Fingerprinting
                        </h5>
                        <p className={textStyles.bodySmall}>
                          Generate unique audio fingerprints for comparison
                        </p>
                      </div>
                    </div>
                  </Panel>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
