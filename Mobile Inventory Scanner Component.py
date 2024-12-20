import React, { useState, useRef, useEffect } from 'react';
import { Camera, RotateCcw, Save } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

const MobileInventoryScanner = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scannedItems, setScannedItems] = useState([]);
  const [error, setError] = useState(null);

  // Start camera stream
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        } 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsScanning(true);
        setError(null);
      }
    } catch (err) {
      setError('Unable to access camera. Please make sure you have granted camera permissions.');
      console.error('Error accessing camera:', err);
    }
  };

  // Stop camera stream
  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsScanning(false);
    }
  };

  // Capture frame and process inventory
  const captureFrame = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      // Set canvas dimensions to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw current video frame to canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // In a real implementation, you would:
      // 1. Send the canvas data to your backend
      // 2. Process with TensorFlow.js or similar
      // 3. Get detection results
      
      // Simulate detection for demo
      const mockDetection = {
        timestamp: new Date().toISOString(),
        items: [
          { id: Date.now(), name: 'Product ' + Math.floor(Math.random() * 100), quantity: Math.floor(Math.random() * 10) + 1 }
        ]
      };

      setScannedItems(prev => [...prev, ...mockDetection.items]);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="w-full max-w-md mx-auto space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="relative aspect-video bg-gray-900 rounded-lg overflow-hidden">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          className="w-full h-full object-cover"
        />
        <canvas
          ref={canvasRef}
          className="hidden"
        />
        
        <div className="absolute bottom-4 left-0 right-0 flex justify-center space-x-4">
          {!isScanning ? (
            <button
              onClick={startCamera}
              className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-full"
            >
              <Camera className="w-5 h-5 mr-2" />
              Start Scanning
            </button>
          ) : (
            <>
              <button
                onClick={stopCamera}
                className="flex items-center px-4 py-2 bg-red-500 text-white rounded-full"
              >
                <RotateCcw className="w-5 h-5 mr-2" />
                Stop
              </button>
              <button
                onClick={captureFrame}
                className="flex items-center px-4 py-2 bg-green-500 text-white rounded-full"
              >
                <Save className="w-5 h-5 mr-2" />
                Capture
              </button>
            </>
          )}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-lg font-semibold mb-4">Scanned Items ({scannedItems.length})</h2>
        <div className="space-y-2">
          {scannedItems.map(item => (
            <div 
              key={item.id}
              className="flex justify-between items-center p-2 bg-gray-50 rounded"
            >
              <span>{item.name}</span>
              <span className="font-medium">Qty: {item.quantity}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MobileInventoryScanner;
