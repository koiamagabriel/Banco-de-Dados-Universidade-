SELECT DISTINCT a.nome AS nome_estudante
FROM alunos a
JOIN cursos c ON a.id_curso = c.id_curso
JOIN departamentos dep ON c.id_departamento = dep.id_departamento
WHERE dep.nome = 'Departamento de Computação';
