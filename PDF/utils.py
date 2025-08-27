from typing import Optional, Literal, Protocol, Sequence, Iterable
from dataclasses import dataclass
from pathlib import Path
import os
import fnmatch

# ---------- 1) 規劃層（只做判斷，不做實際處理） ----------
@dataclass()
class TaskPlan:
    mode: Literal["file", "folder"]         # 要處理單檔或整個資料夾
    input_path: Path                        # 單檔時=檔案路徑；資料夾時=資料夾路徑
    input_dir: Path                         # 基準的輸入資料夾（單檔時 = 檔案所在資料夾）
    output_dir: Path                        # 實際輸出資料夾
    password: Sequence[str]  

@dataclass(frozen=True)
class PipelineConfig:
    patterns: Sequence[str] = ("*.pdf","*.PDF",)   # 要處理哪些檔
    recursive: bool = False                # 是否遞迴子資料夾
    overwrite: bool = True                 # 已存在是否覆蓋
    
# 單檔處理策略介面（由各任務模組實作：remove password、pdf2jpg ...）
class ProcessFilecore(Protocol):
    def __call__(self, input_file: Path, out_file: Path, password: str) -> tuple[bool, str]: ...

class PDFPipeline:
    @classmethod
    def plan_process(cls, input_path: str, output_dir: Optional[str], password: str) -> TaskPlan:
        p = Path(input_path)
        if not p.exists():
            raise ValueError(f"Invalid path (not exists): {p}")

        if p.is_dir():
            inp_dir = p
            out_dir = Path(output_dir) if output_dir else inp_dir
            return TaskPlan(mode="folder", input_path=p, input_dir=inp_dir, output_dir=out_dir, password=password)
        elif p.is_file():
            inp_dir = p.parent
            out_dir = Path(output_dir) if output_dir else inp_dir
            return TaskPlan(mode="file", input_path=p, input_dir=inp_dir, output_dir=out_dir, password=password)
        else:
            raise ValueError(f"Invalid path (neither file nor dir): {p}")
        
    @classmethod
    def process_file_fn(cls, plan: TaskPlan, process_file_core: ProcessFilecore, cfg: PipelineConfig,) -> dict:
        plan.output_dir.mkdir(parents=True, exist_ok=True)
        out_file = plan.output_dir / plan.input_path.name
        if not any(fnmatch.fnmatch(plan.input_path.name, pat) for pat in cfg.patterns):
            result = {}
        elif (not cfg.overwrite) and plan.input_path==out_file:
            result = {"filename": plan.input_path.name, "ok": False, "error": "the same path & can't overwrite"}
        else:
            for pw in plan.password:
                ok, err = process_file_core(plan.input_path, out_file, pw)
                if ok: break
            result = {"filename": plan.input_path.name, "ok": ok, "error": err}
        return result

    @classmethod
    def process_folder(cls, plan: TaskPlan, process_file_core: ProcessFilecore, cfg: PipelineConfig,) -> list[dict]:
        """處理整個資料夾"""
        results = []
        plan_file = plan
        for in_file in _iter_files(plan.input_dir, cfg.patterns, cfg.recursive):
            plan_file.input_path = in_file
            result = cls.process_file_fn(plan_file, process_file_core, cfg)
            if result:
                results.append(result)
        return results

    @classmethod
    def process_file_or_folder(cls, plan: TaskPlan, process_file_core: ProcessFilecore, cfg: PipelineConfig,) -> dict:
        results: list[dict] = []
        if plan.mode == "folder":
            plan.output_dir.mkdir(parents=True, exist_ok=True)
            results = cls.process_folder(plan, process_file_core, cfg)
        else:
            result = cls.process_file_fn(plan, process_file_core, cfg)
            if result:
                results = [result,]
            else:
                print("wrong fike type")

        summary = {
            "files": results,
            "total": len(results),
            "ok": sum(1 for r in results if r["ok"]),
            "fail": sum(1 for r in results if not r["ok"])
        }
        return summary

    @staticmethod
    def print_result(summary: dict) -> None:
        # 輸出每個檔案的結果
        for file in summary["files"]:
            # if file["ok"]:
            #     print(f"✅ {file['filename']}")
            # else:
            if not file["ok"]:
                print(f"❌ {file['filename']}\n error: {file['error']}")
                
        print(" ")
        print(f"total\t: {summary['total']}")
        print(f"ok   \t: {summary['ok']}")
        print(f"fail \t: {summary['fail']}")

    @classmethod
    def process_and_print(cls, input_path: str, output_dir: Optional[str], password: str,
                           process_file_core: ProcessFilecore, 
                           patterns: Sequence[str], recursive: bool, overwrite: bool) -> dict:
        
        """一行搞定：規劃 → 執行 → 列印；並回傳 summary"""
        plan = cls.plan_process(input_path, output_dir, password)
        cfg = PipelineConfig(patterns, recursive, overwrite)
        summary = cls.process_file_or_folder(plan, process_file_core, cfg)
        cls.print_result(summary)
        return summary

# ---------- 通用工具 ----------
def _iter_files(root: Path, patterns: Sequence[str], recursive: bool) -> Iterable[Path]:
    glob = root.rglob if recursive else root.glob
    for pat in patterns:
        yield from (p for p in glob(pat) if p.is_file())
