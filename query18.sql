SELECT DISTINCT a.nome AS nome_estudante
FROM alunos a
JOIN cursos c ON a.id_curso = c.id_curso
JOIN curso_disciplina cd ON c.id_curso = cd.id_curso
JOIN disciplinas d ON cd.id_disciplina = d.id_disciplina
JOIN departamentos dep ON c.id_departamento = dep.id_departamento
WHERE dep.nome LIKE '%Departamento de Matemática%';
