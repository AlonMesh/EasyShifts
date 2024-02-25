export default function Tooltip({ children, show }) {
  return (
    <div className={`tooltip ${show ? 'show' : ''}`}>
      {children}
    </div>
  );
}
