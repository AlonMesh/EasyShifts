function TooltipIcon({ text }) {
  return (
    <span className="tooltip">
      <i className="fas fa-info-circle"></i>

      <span className="tooltiptext">{text}</span>
    </span>
  );
}

export default TooltipIcon;