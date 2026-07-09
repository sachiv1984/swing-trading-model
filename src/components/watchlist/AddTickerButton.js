import PropTypes from "prop-types";
import { Plus } from "lucide-react";
import { Button } from "../ui/button";

export default function AddTickerButton({ onClick }) {
  return (
    <Button
      onClick={onClick}
      className="bg-gradient-to-r from-cyan-500 to-violet-500 hover:from-cyan-400 hover:to-violet-400 text-white border-0 shadow-lg shadow-violet-500/25"
    >
      <Plus className="w-4 h-4 mr-2" />
      Add Ticker
    </Button>
  );
}

AddTickerButton.propTypes = {
  onClick: PropTypes.func.isRequired,
};
