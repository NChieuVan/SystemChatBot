export default function WaveText({ text }) {
  return (
    <span style={{ display: 'inline-block' }}>
      {text.split('').map((ch, i, arr) => (
        <span
          key={i}
          style={{
            display: 'inline-block',
            animation: 'wave 1.2s infinite',
            animationDelay: `${i * 0.08}s`,
            marginRight: i < arr.length - 1 ? (ch === ' ' ? '8px' : '2px') : undefined,
          }}
        >
          {ch}
        </span>
      ))}
      <style>{`
        @keyframes wave {
          0%, 100% { transform: translateY(0); }
          20% { transform: translateY(-7px); }
          40% { transform: translateY(0); }
        }
      `}</style>
    </span>
  );
}