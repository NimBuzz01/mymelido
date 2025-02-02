import { ScanSearch } from "lucide-react";

const LoadingState = () => {
  return (
    <div className="flex flex-col gap-2 h-80 justify-center items-center">
      <ScanSearch className="animate-bounce size-10" />{" "}
      <p className="text-xl">Analyzing your song...</p>
    </div>
  );
};

export default LoadingState;
