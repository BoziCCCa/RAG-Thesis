import React, { useEffect, useState } from "react";

const LoadingDots = () => {
  const [dots, setDots] = useState(".");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prevDots) => (prevDots.length === 4 ? "." : prevDots + "."));
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return <span>{dots}</span>;
};

export default LoadingDots;
