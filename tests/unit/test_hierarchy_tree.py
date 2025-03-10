import pandas as pd

from src.myparser.hierarchy.tree import verify_tree_sp_description_composition_hierarchy, dfs, criar_arvore
from src.myparser.hierarchy.tree import verificar_ciclos, verificar_erros_niveis
from src.myparser.hierarchy.tree import verify_tree_sp_description_composition_levels_childs
from src.myparser.model.spreadsheets import SP_COMPOSITION_COLUMNS, SP_DESCRIPTION_COLUMNS

# DATA FRAMES - GROUND TRUTH
from tests.unit.test_constants import df_sp_description_data_ground_truth_01, df_sp_composition_data_ground_truth_01
from tests.unit.test_constants import df_sp_description_data_ground_truth_05, df_sp_composition_data_ground_truth_05

# DATA FRAMES - ERROS 01
from tests.unit.test_constants import df_sp_description_errors_01, df_sp_composition_errors_01

# DATA FRAMES - ERRORS 09
from tests.unit.test_constants import df_sp_description_errors_09, df_sp_composition_errors_09

# DATA FRAMES - ERROS 16
from tests.unit.test_constants import df_sp_description_errors_16, df_sp_composition_errors_16


def test_true_verify_tree_sp_composition_hierarchy_data_ground_truth_01():
    is_correct, errors, warnings = verify_tree_sp_description_composition_hierarchy(df_sp_composition_data_ground_truth_01, df_sp_description_data_ground_truth_01)
    assert is_correct is True
    assert len(errors) == 0
    assert len(warnings) == 0

def test_true_verify_tree_sp_composition_hierarchy_data_ground_truth_05():
    is_correct, errors, warnings = verify_tree_sp_description_composition_hierarchy(df_sp_composition_data_ground_truth_05, df_sp_description_data_ground_truth_05)
    assert is_correct is True
    assert len(errors) == 0
    assert len(warnings) == 0


def test_count_errors_verify_tree_sp_composition_hierarchy_errors_01():
    is_correct, errors, warnings = verify_tree_sp_description_composition_hierarchy(df_sp_composition_errors_01, df_sp_description_errors_01)
    assert is_correct is False
    assert len(errors) == 1
    assert len(warnings) == 0
    assert errors[0] == 'composicao.xlsx: Ciclo encontrado: [5000 -> 5001 -> 5000].'

def test_count_errors_verify_tree_sp_composition_hierarchy_errors_09():
    is_correct, errors, warnings = verify_tree_sp_description_composition_hierarchy(df_sp_composition_errors_09, df_sp_description_errors_09)
    assert is_correct is False
    assert len(errors) == 4
    assert len(warnings) == 0

    assert errors[0] == 'composicao.xlsx: Ciclo encontrado: [1 -> 2 -> 1].'
    assert errors[1] == 'composicao.xlsx, linha 3: O indicador 2 (nível 2) não pode ser pai do indicador 3 (nível 2). Atualize os níveis no arquivo de descrição.'
    assert errors[2] == 'composicao.xlsx, linha 4: O indicador 2 (nível 2) não pode ser pai do indicador 1 (nível 1). Atualize os níveis no arquivo de descrição.'
    assert errors[3] == 'composicao.xlsx, linha 6: O indicador 3 (nível 2) não pode ser pai do indicador 6 (nível 2). Atualize os níveis no arquivo de descrição.'

def test_criar_arvore_with_no_duplicates():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: [1, 2, 3],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: [2, 3, 4]
    })
    arvore = criar_arvore(composicao)
    assert arvore == {'1': ['2'], '2': ['3'], '3': ['4']}

def test_criar_arvore_with_duplicates():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: [1, 1, 2, 2, 3, 3],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: [2, 2, 3, 3, 4, 4]
    })
    arvore = criar_arvore(composicao)
    assert arvore == {'1': ['2', '2'], '2': ['3', '3'], '3': ['4', '4']}

def test_criar_arvore_with_string_values():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: ['1000', '2000', '3000'],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: ['2000', '3000', '4000']
    })
    arvore = criar_arvore(composicao)
    assert arvore == {'1000': ['2000'], '2000': ['3000'], '3000': ['4000']}

def test_dfs_with_no_cycle():
    arvore = {'1': ['2'], '2': ['3'], '3': ['4']}
    visitado = set()
    caminho_atual = []
    ciclo_encontrado, ciclo = dfs(arvore, '1', visitado, caminho_atual)
    assert ciclo_encontrado is False
    assert ciclo == []

def test_dfs_with_cycle():
    arvore = {'1': ['2'], '2': ['3'], '3': ['1']}
    visitado = set()
    caminho_atual = []
    ciclo_encontrado, ciclo = dfs(arvore, '1', visitado, caminho_atual)
    assert ciclo_encontrado is True
    assert ciclo == ['1', '2', '3', '1']

def test_dfs_with_multiple_branches_and_no_cycle():
    arvore = {'1': ['2', '3'], '2': ['4'], '3': ['5']}
    visitado = set()
    caminho_atual = []
    ciclo_encontrado, ciclo = dfs(arvore, '1', visitado, caminho_atual)
    assert ciclo_encontrado is False
    assert ciclo == []

def test_dfs_with_multiple_branches_and_cycle():
    arvore = {'1': ['2', '3'], '2': ['4'], '3': ['1']}
    visitado = set()
    caminho_atual = []
    ciclo_encontrado, ciclo = dfs(arvore, '1', visitado, caminho_atual)
    assert ciclo_encontrado is True
    assert ciclo == ['1', '3', '1']

def test_verificar_ciclos_with_no_cycle():
    arvore = {'1': ['2'], '2': ['3'], '3': ['4']}
    ciclo_encontrado, ciclo = verificar_ciclos(arvore)
    assert ciclo_encontrado is False
    assert ciclo == []

def test_verificar_ciclos_with_cycle():
    arvore = {'1': ['2'], '2': ['3'], '3': ['1']}
    ciclo_encontrado, ciclo = verificar_ciclos(arvore)
    assert ciclo_encontrado is True
    assert ciclo == ['1', '2', '3', '1']

def test_verificar_ciclos_with_multiple_branches_and_no_cycle():
    arvore = {'1': ['2', '3'], '2': ['4'], '3': ['5']}
    ciclo_encontrado, ciclo = verificar_ciclos(arvore)
    assert ciclo_encontrado is False
    assert ciclo == []

def test_verificar_ciclos_with_multiple_branches_and_cycle():
    arvore = {'1': ['2', '3'], '2': ['4'], '3': ['1']}
    ciclo_encontrado, ciclo = verificar_ciclos(arvore)
    assert ciclo_encontrado is True
    assert ciclo == ['1', '3', '1']

def test_verificar_erros_niveis_with_no_errors():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: ['1000', '2000', '3000'],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: ['2000', '3000', '4000']
    })
    descricao = pd.DataFrame({
        SP_DESCRIPTION_COLUMNS.CODIGO: ['1000', '2000', '3000', '4000'],
        SP_DESCRIPTION_COLUMNS.NIVEL: [1, 2, 3, 4]
    })
    erros = verificar_erros_niveis(composicao, descricao)
    assert erros == []

def test_verificar_erros_niveis_with_errors():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: ['1000', '2000', '3000'],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: ['2000', '3000', '4000']
    })
    descricao = pd.DataFrame({
        SP_DESCRIPTION_COLUMNS.CODIGO: ['1000', '2000', '3000', '4000'],
        SP_DESCRIPTION_COLUMNS.NIVEL: [1, 2, 2, 4]
    })
    erros = verificar_erros_niveis(composicao, descricao)
    assert erros == [('2000', '3000')]

def test_verificar_erros_niveis_with_missing_levels():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: ['1000', '2000', '3000'],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: ['2000', '3000', '4000']
    })
    descricao = pd.DataFrame({
        SP_DESCRIPTION_COLUMNS.CODIGO: ['1000', '2000', '4000'],
        SP_DESCRIPTION_COLUMNS.NIVEL: [1, 2, 4]
    })
    erros = verificar_erros_niveis(composicao, descricao)
    assert erros == [(None, '3000'), ('3000', None)]

def test_verificar_erros_niveis_with_major_levels():
    composicao = pd.DataFrame({
        SP_COMPOSITION_COLUMNS.CODIGO_PAI: ['1000', '2000', '3000'],
        SP_COMPOSITION_COLUMNS.CODIGO_FILHO: ['2000', '3000', '4000']
    })
    descricao = pd.DataFrame({
        SP_DESCRIPTION_COLUMNS.CODIGO: ['1000', '2000', '3000', '4000'],
        SP_DESCRIPTION_COLUMNS.NIVEL: [1, 2, 77, 88]
    })
    erros = verificar_erros_niveis(composicao, descricao)
    assert len(erros) == 0

# Testes para def verify_tree_sp_description_composition_levels_childs(df_composicao, df_descricao):
def test_true_verify_tree_sp_description_composition_levels_childs_data_ground_truth_01():
    is_correct, errors, warnings = verify_tree_sp_description_composition_levels_childs(df_sp_composition_data_ground_truth_01, df_sp_description_data_ground_truth_01)
    assert is_correct is True
    assert len(errors) == 0
    assert len(warnings) == 0

def test_count_errors_verify_tree_sp_description_composition_levels_childs_errors_16():
    is_correct, errors, warnings = verify_tree_sp_description_composition_levels_childs(df_sp_composition_errors_16, df_sp_description_errors_16)
    assert is_correct is False
    assert len(errors) == 1
    assert len(warnings) == 0
    assert errors[0] == "descricao.xlsx: Indicadores filhos do pai 6 não estão no mesmo nível: [indicador 8 possui nível '5', indicador 9 possui nível '200']."
