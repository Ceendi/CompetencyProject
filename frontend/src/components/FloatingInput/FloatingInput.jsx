import "./FloatingInput.css";

export default function FloatingInput({
  id,
  label,
  value,
  onChange,
  disabled = false,
  type = "text",
}) {
  return (
    <div className="floating-input-wrapper">
      <input
        type={type}
        className="floating-input"
        placeholder=" "
        value={value}
        onChange={onChange}
        disabled={disabled}
        id={id}
      />
      <label htmlFor={id} className="floating-input-label">
        {label}
      </label>
    </div>
  );
}
