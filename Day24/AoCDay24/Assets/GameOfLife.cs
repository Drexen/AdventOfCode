using System.Linq;
using System.Collections.Generic;
using UnityEngine;

public class GameOfLife : MonoBehaviour
{
    [SerializeField] private TextAsset m_input = null;
    [SerializeField] private GameObject m_prefabCell = null;

    private Dictionary<int, bool?[,]> m_boards = new Dictionary<int, bool?[,]>();
    private Dictionary<int, Cell[,]> m_cells = new Dictionary<int, Cell[,]>();
    private Vector2 m_boardSize;
    private float m_lastUpdate = 0f;
    bool m_running = true;

    private void Awake()
    {
        var lines = m_input.text.Split('\n').Select(x=>x.Replace("\r", "")).ToArray();
        m_boardSize = new Vector2(lines.Length, lines[0].Length);
        var board = new bool?[(int)m_boardSize.x, (int)m_boardSize.y];
        for(int l = 0; l < lines.Length; ++l)
        {
            for(int c = 0; c < lines[l].Length; c++)
            {
                board[c, l] = (lines[l][c] == '.' ? false : true);
            }
        }

        board[2, 2] = null;

        m_boards.Add(0, board);
        m_cells.Add(0, CreateCellsForDepth(0));

        //UpdateAllBoardsVisually();
    }

    private Cell[,] CreateCellsForDepth(int depth)
    {
        GameObject container = new GameObject("Depth_" + depth);
        container.transform.parent = transform;
        var cells = new Cell[5, 5];
        for(int y = 0; y < 5; ++y)
        {
            for(int x = 0; x < 5; ++x)
            {
                if(x != 2 || y != 2)
                {
                    GameObject cellObj = GameObject.Instantiate(m_prefabCell, container.transform);
                    cellObj.transform.localPosition = new Vector3(x, -y, -(depth * 5f));
                    var cell = cellObj.GetComponent<Cell>();
                    cells[x, y] = cell;
                }
            }
        }
        return cells;
    }

    int tick = 0;
    private void Update()
    {
        if(m_running == true)
        {
            float delta = (Time.time - m_lastUpdate);
            if(delta > 0f)
            {
                m_lastUpdate = Time.time;
                if(tick == 200)
                {
                    m_running = false;

                    int totalBugs = GetTotalBugs();
                    Debug.Log("Total bugs = " + totalBugs);
                    Debug.Log("Num boards = " + m_boards.Count);
                }
                else
                {
                    ++tick;
                    UpdateAllBoardsLogically();
                    //UpdateAllBoardsVisually();
                }
            }
        }
    }

    private int GetTotalBugs()
    {
        return m_boards.Sum(i => i.Value.Cast<bool?>().Count(b => b == true));
    }

    private void UpdateAllBoardsLogically()
    {
        Dictionary<int, bool?[,]> newBoards = new Dictionary<int, bool?[,]>();

        var e = m_boards.Keys.OrderBy(b => b);
        int first = e.First();
        int last = e.Last();
        bool?[,] board = new bool?[5, 5];
        for(int y = 0; y < 5; ++y)
        {
            for(int x = 0; x < 5; ++x)
            {
                if(x == 2 && y == 2)
                {
                    board[x, y] = null;
                }
                else
                {
                    board[x, y] = false;
                }
            }
        }
        m_boards.Add(first - 1, board);
        m_boards.Add(last + 1, (bool?[,])board.Clone());

        foreach(var b in m_boards)
        {
            var newBoard = UpdateBoardLogically(m_boards, b.Key);
            newBoards.Add(b.Key, newBoard);
        }

        m_boards = newBoards;
    }

    private void UpdateAllBoardsVisually()
    {
        foreach(var i in m_boards)
        {
            if(m_cells.ContainsKey(i.Key) == false)
            {
                m_cells.Add(i.Key, CreateCellsForDepth(i.Key));
            }
        }

        foreach(var i in m_cells)
        {
            UpdateBoardVisually(i.Key);
        }
    }

    private static bool?[,] UpdateBoardLogically(Dictionary<int, bool?[,]> boards, int targetDepth)
    {
        bool?[,] boardCopy = (bool?[,])boards[targetDepth].Clone();
        for(int y = 0; y < 5; ++y)
        {
            for(int x = 0; x < 5; ++x)
            {
                if(boardCopy[x, y] != null)
                {
                    int numAdjacents = GetNumAdjacentBugs(boards, targetDepth, x, y);
                    Debug.Assert(numAdjacents <= 8);
                    if(boards[targetDepth][x, y] == true)
                    {
                        if(numAdjacents != 1)
                        {
                            boardCopy[x, y] = false;
                        }
                    }
                    else
                    {
                        if(numAdjacents == 1 || numAdjacents == 2)
                        {
                            boardCopy[x, y] = true;
                        }
                    }
                }
            }
        }

        return boardCopy;
    }

    private void UpdateBoardVisually(int depth)
    {
        for(int y = 0; y < m_boardSize.y; ++y)
        {
            for(int x = 0; x < m_boardSize.x; ++x)
            {
                if(x != 2 || y != 2)
                {
                    m_cells[depth][x, y].gameObject.SetActive(m_boards[depth][x, y] == true);
                }
            }
        }
    }

    private static int GetNumAdjacentBugs(Dictionary<int, bool?[,]> boards, int targetDepth, int x, int y)
    {
        int output = 0;
        var board = boards[targetDepth];

        if(x == 1 && y == 2)
        {
            if(boards.ContainsKey(targetDepth - 1) == true)
            {
                for(int y2 = 0; y2 < 5; ++y2)
                {
                    if(boards[targetDepth - 1][0, y2] == true) output++;
                }
            }
        }
        else if(x == 3 && y == 2)
        {
            if(boards.ContainsKey(targetDepth - 1) == true)
            {
                for(int y2 = 0; y2 < 5; ++y2)
                {
                    if(boards[targetDepth - 1][4, y2] == true) output++;
                }
            }
        }
        else if(x == 2 && y == 1)
        {
            if(boards.ContainsKey(targetDepth - 1) == true)
            {
                for(int x2 = 0; x2 < 5; ++x2)
                {
                    if(boards[targetDepth - 1][x2, 0] == true) output++;
                }
            }
        }
        else if(x == 2 && y == 3)
        {
            if(boards.ContainsKey(targetDepth - 1) == true)
            {
                for(int x2 = 0; x2 < 5; ++x2)
                {
                    if(boards[targetDepth - 1][x2, 4] == true) output++;
                }
            }
        }
        
        if(x > 0)
        {
            if(board[x - 1, y] == true) output++;
        }
        else
        {
            if(boards.ContainsKey(targetDepth + 1) == true)
            {
                if(boards[targetDepth + 1][1, 2] == true) output++;
            }
        }

        if(x + 1 < 5)
        {
            if(board[x + 1, y] == true) output++;
        }
        else
        {
            if(boards.ContainsKey(targetDepth + 1) == true)
            {
                if(boards[targetDepth + 1][3, 2] == true) output++;
            }
        }

        if(y > 0)
        {
            if(board[x, y - 1] == true) output++;
        }
        else
        {
            if(boards.ContainsKey(targetDepth + 1) == true)
            {
                if(boards[targetDepth + 1][2, 1] == true) output++;
            }
        }

        if(y + 1 < 5)
        {
            if(board[x, y + 1] == true) output++;
        }
        else
        {
            if(boards.ContainsKey(targetDepth + 1) == true)
            {
                if(boards[targetDepth + 1][2, 3] == true) output++;
            }
        }

        return output;
    }
}
