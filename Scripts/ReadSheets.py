"""
Script de teste para validar a funcionalidade de Feriados.
Testa tanto feriados nacionais quanto municipais do Google Sheets.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from Feriados import Feriados


def testar_feriados_nacionais():
    """Testa o carregamento de feriados nacionais via API"""
    print("=" * 80)
    print("TESTE 1: Feriados Nacionais (Brasil API)")
    print("=" * 80)
    
    feriados = Feriados(ano=2025)
    feriados._carregar_feriados_nacionais()
    
    if feriados._cache_datas_nacionais:
        print(f"\n✓ Total de feriados nacionais em 2025: {len(feriados._cache_datas_nacionais)}")
        print("\nLista de feriados nacionais:")
        for data in sorted(feriados._cache_datas_nacionais):
            print(f"  - {data}")
    else:
        print("✗ Nenhum feriado nacional encontrado ou erro na API")
    
    print()


def testar_feriados_municipais():
    """Testa o carregamento de feriados municipais do Google Sheets"""
    print("=" * 80)
    print("TESTE 2: Feriados Municipais (Google Sheets)")
    print("=" * 80)
    
    municipal_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv"
    )
    
    feriados = Feriados(
        ano=2025,
        municipal_csv_url=municipal_csv_url,
        municipal_date_column="date"
    )
    
    feriados._carregar_feriados_municipais()
    
    if feriados._cache_datas_municipais:
        print(f"\n✓ Total de feriados municipais em 2025: {len(feriados._cache_datas_municipais)}")
        print("\nLista de feriados municipais:")
        for data in sorted(feriados._cache_datas_municipais):
            print(f"  - {data}")
    else:
        print("✗ Nenhum feriado municipal encontrado ou erro ao ler Google Sheets")
    
    print()


def testar_todos_feriados():
    """Testa a combinação de todos os feriados (nacionais + municipais)"""
    print("=" * 80)
    print("TESTE 3: Todos os Feriados (Nacionais + Municipais)")
    print("=" * 80)
    
    municipal_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv"
    )
    
    feriados = Feriados(
        ano=2025,
        municipal_csv_url=municipal_csv_url,
        municipal_date_column="date"
    )
    
    todos_feriados = feriados.get_feriados()
    
    if todos_feriados:
        print(f"\n✓ Total de feriados (nacionais + municipais): {len(todos_feriados)}")
        print("\nLista completa de feriados em 2025:")
        for data in todos_feriados:
            print(f"  - {data}")
    else:
        print("✗ Nenhum feriado encontrado")
    
    print()


def testar_hoje():
    """Testa se hoje é feriado"""
    print("=" * 80)
    print("TESTE 4: Verificação de Hoje")
    print("=" * 80)
    
    municipal_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv"
    )
    
    feriados = Feriados(
        municipal_csv_url=municipal_csv_url,
        municipal_date_column="date"
    )
    
    hoje = datetime.now(tz=ZoneInfo("America/Sao_Paulo"))
    hoje_str = hoje.strftime("%Y-%m-%d")
    dia_semana = hoje.strftime("%A")
    
    print(f"\nData de hoje: {hoje_str} ({dia_semana})")
    
    is_feriado = feriados.is_feriado_hoje()
    print(f"É feriado hoje? {'✓ SIM' if is_feriado else '✗ NÃO'}")
    
    pode_bater, mensagem = feriados.can_mark_today()
    print(f"\nPode bater ponto hoje? {'✓ SIM' if pode_bater else '✗ NÃO'}")
    print(f"Motivo: {mensagem}")
    
    print()


def testar_datas_especificas():
    """Testa datas específicas conhecidas (Natal, Ano Novo, etc.)"""
    print("=" * 80)
    print("TESTE 5: Verificação de Datas Específicas")
    print("=" * 80)
    
    municipal_csv_url = (
        "https://docs.google.com/spreadsheets/d/"
        "14-6PkC3XyFaSXk7WcZzsum0uBevVQfp1h063dFEOffE/export?format=csv"
    )
    
    feriados = Feriados(
        ano=2025,
        municipal_csv_url=municipal_csv_url,
        municipal_date_column="date"
    )
    
    todos_feriados = feriados.get_feriados()
    
    datas_teste = {
        "2025-01-01": "Ano Novo",
        "2025-12-25": "Natal",
        "2025-04-21": "Tiradentes",
        "2025-09-07": "Independência do Brasil",
        "2025-11-15": "Proclamação da República",
    }
    
    print("\nVerificando datas conhecidas:")
    for data, nome in datas_teste.items():
        eh_feriado = data in todos_feriados
        status = "✓ É FERIADO" if eh_feriado else "✗ Não é feriado"
        print(f"  {data} ({nome}): {status}")
    
    print()


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SUITE DE TESTES - FERIADOS" + " " * 32 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    try:
        testar_feriados_nacionais()
        testar_feriados_municipais()
        testar_todos_feriados()
        testar_hoje()
        testar_datas_especificas()
        
        print("=" * 80)
        print("✓ TODOS OS TESTES CONCLUÍDOS")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()