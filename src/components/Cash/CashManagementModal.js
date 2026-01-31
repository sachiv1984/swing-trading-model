import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { base44 } from "@/api/base44Client";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PlusCircle, MinusCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

export default function CashManagementModal({ open, onClose, portfolio, transactions }) {
  const [type, setType] = useState("deposit");
  const [amount, setAmount] = useState("");
  const [note, setNote] = useState("");
  const queryClient = useQueryClient();

  const createTransaction = useMutation({
    mutationFn: async (data) => {
      await base44.entities.CashTransaction.create(data);
      
      const newBalance = type === "withdrawal" 
        ? (portfolio?.cash_balance || 0) - parseFloat(amount)
        : (portfolio?.cash_balance || 0) + parseFloat(amount);
      
      if (portfolio?.id) {
        await base44.entities.Portfolio.update(portfolio.id, { 
          cash_balance: newBalance
        });
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["portfolios"] });
      queryClient.invalidateQueries({ queryKey: ["cashTransactions"] });
      setAmount("");
      setNote("");
      onClose();
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;
    
    createTransaction.mutate({
      type,
      amount: parseFloat(amount),
      note,
      date: new Date().toISOString().split("T")[0]
    });
  };

  const recentTransactions = transactions?.slice(0, 5) || [];

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="bg-slate-900 border-slate-800 text-white max-w-md">
        <DialogHeader>
          <DialogTitle>Cash Management</DialogTitle>
        </DialogHeader>

        <div className="mb-4 p-4 rounded-xl bg-slate-800/50 border border-slate-700">
          <p className="text-sm text-slate-400">Current Cash Balance</p>
          <p className="text-2xl font-bold text-white">
            £{(portfolio?.cash_balance || 0).toLocaleString("en-GB", { minimumFractionDigits: 2 })}
          </p>
        </div>

        <Tabs value={type} onValueChange={setType}>
          <TabsList className="grid grid-cols-2 bg-slate-800">
            <TabsTrigger value="deposit" className="data-[state=active]:bg-emerald-500/20 data-[state=active]:text-emerald-400">
              <PlusCircle className="w-4 h-4 mr-2" />
              Deposit
            </TabsTrigger>
            <TabsTrigger value="withdrawal" className="data-[state=active]:bg-rose-500/20 data-[state=active]:text-rose-400">
              <MinusCircle className="w-4 h-4 mr-2" />
              Withdraw
            </TabsTrigger>
          </TabsList>

          <form onSubmit={handleSubmit} className="mt-4 space-y-4">
            <div>
              <Label htmlFor="amount">Amount (£)</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                min="0"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="bg-slate-800 border-slate-700 mt-1"
              />
            </div>
            <div>
              <Label htmlFor="note">Note (optional)</Label>
              <Input
                id="note"
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="e.g., Monthly deposit"
                className="bg-slate-800 border-slate-700 mt-1"
              />
            </div>
            <Button 
              type="submit" 
              disabled={createTransaction.isPending || !amount}
              className={cn(
                "w-full",
                type === "deposit" 
                  ? "bg-emerald-600 hover:bg-emerald-700" 
                  : "bg-rose-600 hover:bg-rose-700"
              )}
            >
              {createTransaction.isPending && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
              {type === "deposit" ? "Add Funds" : "Withdraw Funds"}
            </Button>
          </form>
        </Tabs>

        {recentTransactions.length > 0 && (
          <div className="mt-6 pt-4 border-t border-slate-800">
            <p className="text-sm font-medium text-slate-400 mb-3">Recent Transactions</p>
            <div className="space-y-2">
              {recentTransactions.map((tx) => (
                <div key={tx.id} className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    {tx.type === "withdrawal" ? (
                      <MinusCircle className="w-4 h-4 text-rose-400" />
                    ) : (
                      <PlusCircle className="w-4 h-4 text-emerald-400" />
                    )}
                    <span className="text-slate-300">{tx.note || tx.type}</span>
                  </div>
                  <span className={tx.type === "withdrawal" ? "text-rose-400" : "text-emerald-400"}>
                    {tx.type === "withdrawal" ? "-" : "+"}£{tx.amount.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
